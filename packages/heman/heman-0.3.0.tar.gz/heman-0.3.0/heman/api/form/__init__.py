import json
import locale

from flask import request, Response, jsonify

from heman.api import AuthorizedResource
from heman.auth import check_cups_allowed, check_contract_allowed
from heman.config import peek


TYPES_MAP = {
    'integer': 'integer',
    'char': 'string',
    'selection': 'string',
    'boolean': 'boolean'
}


def get_first_lang():
    """Get the first lang of Accept-Language Header.
    """
    request_lang = request.headers.get('Accept-Language').split(',')
    if request_lang:
        lang = locale.normalize(request_lang[0]).split('.')[0]
    else:
        lang = False
    return lang


def jsonform(definition):
    res = {'schema': {}, 'form': []}
    schema = res['schema']
    form = res['form']
    for name, fdef in definition.items():
        if fdef['type'] not in TYPES_MAP:
            continue
        schema[name] = {
            'type': TYPES_MAP[fdef['type']],
            'title': fdef['string'],
            'description': fdef.get('help'),
            'required': fdef.get('required', False)
        }
        selection = fdef.get('selection')
        if selection:
            enum = []
            title_map = {}
            for key, value in selection:
                enum.append(key)
                title_map[key] = value
            schema[name]['enum'] = enum
            form.append({
                'key': name,
                'titleMap': title_map
            })
        else:
            form.append({'key': name})
    form.append({'type': 'submit', 'title': 'Enviar'})
    return res


class AuthorizedByCupsResource(AuthorizedResource):
    method_decorators = (
        AuthorizedResource.method_decorators + [check_cups_allowed]
    )


class AuthorizedByContractResource(AuthorizedResource):
    method_decorators = (
        AuthorizedResource.method_decorators + [check_contract_allowed]
    )


class FormResource(AuthorizedResource):
    pass


class EmpoweringBuildingDefForm(FormResource):
    def get(self):
        lang = get_first_lang()
        model = peek.model('empowering.cups.building')
        def_fields = model.fields_get([], context={'lang': lang})
        def_fields.pop('meteringPointId', None)
        res = jsonform(def_fields)
        return Response(json.dumps(res), mimetype='application/json')


class EmpoweringBuildingForm(FormResource, AuthorizedByCupsResource):
    def get(self, cups):
        model = peek.model('empowering.cups.building')
        cups_ids = model.search([('cups_id.name', '=', cups)])
        if not cups_ids:
            res = {}
        else:
            res = model.read(cups_ids[0])
        return Response(json.dumps(res), mimetype='application/json')

    def post(self, cups):
        model = peek.model('empowering.cups.building')
        building_ids = model.search([('cups_id.name', '=', cups)])
        data = request.json
        if not building_ids:
            cups = peek.model('giscedata.cups.ps').search([
                ('name', '=', cups)
            ])
            if not cups:
                return jsonify({'status': 404, 'message': 'Not Found'}), 404
            data['cups_id'] = cups[0]
            model.create(data)
        else:
            model.write(building_ids, data)
        return jsonify({'status': 200, 'message': 'OK'}), 200


class EmpoweringProfileDefForm(FormResource):
    def get(self):
        lang = get_first_lang()
        model = peek.model('empowering.modcontractual.profile')
        def_fields = model.fields_get([], context={'lang': lang})
        def_fields.pop('femalePersonsNumber', None)
        def_fields.pop('malePersonsNumber', None)
        def_fields.pop('eduLevel_sec', None)
        def_fields.pop('eduLevel_noStudies', None)
        def_fields.pop('eduLevel_prim', None)
        def_fields.pop('eduLevel_uni', None)
        res = jsonform(def_fields)
        return Response(json.dumps(res), mimetype='application/json')


class EmpoweringProfileForm(FormResource, AuthorizedByContractResource):
    def get(self, contract):
        model = peek.model('empowering.modcontractual.profile')
        profile_ids = model.search([
            ('modcontractual_id.polissa_id.name', '=', contract)
        ])
        if not profile_ids:
            res = {}
        else:
            res = model.read(profile_ids[0])
        return Response(json.dumps(res), mimetype='application/json')

    def post(self, contract):
        model = peek.model('empowering.modcontractual.profile')
        profile_ids = model.search([
            ('modcontractual_id.polissa_id.name', '=', contract)
        ])
        data = request.json
        contract_obj = peek.model('giscedata.polissa')
        con_id = contract_obj.search([('name', '=', contract)])
        if not con_id:
            return jsonify({'status': 404, 'message': 'Not Found'}), 404
        contract = contract_obj.browse(con_id[0])
        if not profile_ids:
            mod = contract.modcontractual_activa.id
            data['modcontractual_id'] = mod
            profile_id = model.create(data)
        else:
            profile_id = profile_ids[0]
            model.write([profile_id], data)
        contract.write({'empowering_profile': profile_id})
        return jsonify({'status': 200, 'message': 'OK'}), 200


class EmpoweringSettingsDefForm(FormResource):
    def get(self):
        lang = get_first_lang()
        model = peek.model('giscedata.cups.ps')
        def_fields = model.fields_get(['empowering'], context={'lang': lang})
        res = jsonform(def_fields)
        return Response(json.dumps(res), mimetype='application/json')


class EmpoweringSettingsForm(FormResource, AuthorizedByContractResource):
    def get(self, contract):
        contract_obj = peek.model('giscedata.polissa')
        contract_ids = contract_obj.search([
            ('name', '=', contract)
        ])
        if not contract_ids:
            res = {}
        else:
            cups_id = contract_obj.read(contract_ids[0], ['cups'])['cups'][0]
            cups_obj = peek.model('giscedata.cups.ps')
            res = cups_obj.read(cups_id, ['empowering'])
        return Response(json.dumps(res), mimetype='application/json')

    def post(self, contract):
        data = request.json
        contract_obj = peek.model('giscedata.polissa')
        con_id = contract_obj.search([('name', '=', contract)])
        if not con_id:
            return jsonify({'status': 404, 'message': 'Not Found'}), 404
        cups_id = contract_obj.read(con_id, ['cups'])[0]['cups'][0]
   
        if 'empowering' not in data or not isinstance(data['empowering'], bool):  
            return jsonify({'status': 404, 'message': 'Data missing'}), 404

        cups_obj = peek.model('giscedata.cups.ps')
        cups_obj.write([cups_id], {'empowering': data['empowering']})
        return jsonify({'status': 200, 'message': 'OK'}), 200
resources = [
    (EmpoweringBuildingDefForm, '/EmpoweringBuildingDefForm'),
    (EmpoweringBuildingForm, '/EmpoweringBuildingForm/<cups>'),
    (EmpoweringProfileDefForm, '/EmpoweringProfileDefForm'),
    (EmpoweringProfileForm, '/EmpoweringProfileForm/<contract>'),
    (EmpoweringSettingsDefForm, '/EmpoweringSettingsDefForm'),
    (EmpoweringSettingsForm, '/EmpoweringSettingsForm/<contract>')
]
