# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import string


class Controller(http.Controller):
    lead_fields_mapping = {
        "title": "name", "country": "country_id", "company_name": "partner_name", "industry": "lp_lead_industry",
        "job_position": "function", "email": "email_from", "Persona": "persona"
    }
    lead_required_fields = ["title", "company_name", "country", "industry", "contact_name", "email", "job_position"
        , "phone", "mobile", "mql_score", "autopilot_create_date", "lifecycle_stage", "Persona",
                            "request_demo_msg"]

    contact_required_fields = ["company_id", "company_name", "company_domain", "country", "industry", "contact_name",
                               "email",
                               "job_position", "phone", "mobile"]

    @http.route('/generate_lead', methods=["POST"], type='json', auth="api_key")
    def generate_lead(self, **kwargs):
        lead_obj = request.env["crm.lead"]
        if all(attr in kwargs for attr in self.lead_required_fields):
            country = request.env["res.country"].search([("code", '=', kwargs.get("country").upper())], limit=1)
            department = request.env["hr.department"].search([('lp_category', '=', 'sales_and_marketing')], limit=1)
            industry = request.env[ 'res.partner.industry'].search([('name','=',kwargs.get("industry"))])
            vals = {self.lead_fields_mapping.get(field, field): kwargs.get(field) for field in self.lead_required_fields \
                    if field != "country"}
            vals.update({"country_id": country.id, "created_externally": True, 'lp_department': department.id,'lp_lead_industry':industry.id,
                         "referred": request.auth_api_key_name})
            try:
                lead = lead_obj.create(vals)
                return {"lead_id": lead.id, "status_code": 200}
            except Exception as e:
                return {"status_code": 400, "failure_message": e}
        else:
            not_provided_fields = [xfield for xfield in self.lead_required_fields if xfield not in kwargs]
            fmessage = ','.join(not_provided_fields) + " field/s is/are required."
            return {"status_code": 400, "failure_message": fmessage}

    @http.route('/create_contact', type='json', methods=["POST"], auth="api_key")
    def create_contact(self, **kwargs):
        try:
            partner_obj = request.env["res.partner"]
            if all(attr in kwargs for attr in self.contact_required_fields):
                company_id = kwargs.get("company_id")
                company_name = kwargs.get("company_name")

                country = request.env["res.country"].search([("code", "=", kwargs.get("country").upper())], limit=1)
                industry = request.env["res.partner.industry"].search([('name', '=', kwargs.get("industry"))], limit=1)
                company_vals = {"name": kwargs.get("company_name", False), "country_id": country.id,
                                "email": kwargs.get("email"), "lp_domain": kwargs.get("company_domain"),
                                "phone": kwargs.get("phone", False), "mobile": kwargs.get("mobile", False),
                                "industry_id": industry.id
                    , "company_type": "company", "created_externally": True, "referred": request.auth_api_key_name}



                company = None

                if company_id:
                    search_company = partner_obj.search([("id", '=', company_id)])
                    if search_company:
                        search_company.update(company_vals)
                        company = search_company
                    else:
                        return {"status_code": 400, "failure_message": "Company With This Id Is Not Exist"}

                elif company_name and not company_id:
                    company_domain = kwargs.get("company_domain")
                    search_company = partner_obj.search(
                        [("lp_domain", '=', company_domain), ('is_company', '=', True)], limit=1)
                    if search_company:
                        search_company.update(company_vals)
                        company = search_company

                if not company:
                    company = partner_obj.create(company_vals)

                    partner_vals = {"name": kwargs.get("contact_name", False), "country_id": country.id,
                                    "phone": kwargs.get("phone", False), "mobile": kwargs.get("mobile", False),
                                    "email": kwargs.get("email", False), "company_type": "person",
                                    "parent_id": company.id,"function": kwargs.get("job_position",False),
                                    "created_externally": True, "referred": request.auth_api_key_name}

                    contact = partner_obj.create(partner_vals)
                    return {"contact_id": contact.id, 'company_id': company.id, "status_code": 200}


                partner_vals = {"name": kwargs.get("contact_name", False), "country_id": country.id,
                                "phone": kwargs.get("phone", False), "mobile": kwargs.get("mobile", False),
                                "email": kwargs.get("email", False), "company_type": "person",
                                "parent_id": company.id,"function": kwargs.get("job_position",False),
                                "created_externally": True, "referred": request.auth_api_key_name}

                contact_is_exist = partner_obj.search(
                    [("email", '=', kwargs.get("email", False)), ('is_company', '=', False)], limit=1)

                if contact_is_exist:
                    contact_is_exist.update(partner_vals)
                    return {"contact_id": contact_is_exist.id, 'company_id': company.id, "status_code": 200}
                else:
                    contact = partner_obj.create(partner_vals)
                    return {"contact_id": contact.id, 'company_id': company.id, "status_code": 200}

            else:
                not_provided_fields = [xfield for xfield in self.contact_required_fields if xfield not in kwargs]
                fmessage = ','.join(not_provided_fields) + " field/s is/are not provided from your side"
                return {"status_code": 400, "failure_message": fmessage}
        except Exception as fmessage:
            return {"status_code": 400, "failure_message": fmessage}



    @http.route('/update_lead', type='json', methods=["PUT"], auth="api_key")
    def update_lead(self, **kwargs):
        lead_id = kwargs.get("lead_id")
        if not lead_id:
            return {"status_code": 400, "failure_message": "lead_id is not provided from your side."}
        if type(lead_id) is not int:
            return {"status_code": 400, "failure_message": "lead_id should be integer."}
        new_score = kwargs.get("mql_score", False)
        new_stage = kwargs.get("lifecycle_stage", False)
        vals = {}
        lead = request.env["crm.lead"].search([('id', '=', lead_id), ('created_externally', '=', True)], limit=1)
        if lead:
            if new_score:
                vals["mql_score"] = new_score
            if new_stage:
                vals["lifecycle_stage"] = new_stage
            if vals:
                try:
                    lead.write(vals)
                    return {"status_code": 200}
                except Exception as e:
                    return {"status_code": 400, "failure_message": e}
            else:
                return {"status_code": 400,
                        "failure_message": "field/s to be updated is/are not provided from your side."}
        else:
            return {"status_code": 400, "failure_message": "lead_id is not exist."}


    @http.route('/search_lead', type='json', methods=["POST"], auth="api_key")
    def search_lead(self, **kwargs):
        search_term = kwargs.get("search_term").strip()
        if search_term:
            auth_api_key = request.auth_api_key_name
            leads = request.env['crm.lead'].search(['&',
                                                    '&',
                                                    ('referred', '=', auth_api_key),
                                                    ('created_externally', '=', True),
                                                    '|', '|', '|',
                                                    ('name', '=', search_term),
                                                    ('phone', '=', search_term),
                                                    ('contact_name', '=', search_term),
                                                    ('email_from', '=', search_term),
                                                    ])

            list_of_leads = []
            for lead in leads:
                list_of_leads.append(
                    {"title": lead.name, "company_name": lead.partner_name, "country": lead.country_id.name,
                     "industry": lead.lp_lead_industry.name, "contact_name": lead.contact_name,
                     "email": lead.email_from,
                     "job_position": lead.function, "phone": lead.phone, "mobile": lead.mobile,
                     "mql_score": lead.mql_score,
                     "autopilot_create_date": lead.autopilot_create_date,
                     "lifecycle_stage": lead.lifecycle_stage,
                     "Persona": lead.persona,
                     "request_demo_msg": lead.request_demo_msg})

            if list_of_leads:
                return {"leads": list_of_leads, "status_code": 200}
            else:
                return {"status_code": 400, "failure_message": "Lead is not exist."}

        else:
            return {"status_code": 400, "failure_message": " field search_term is not provided from your side"}


    @http.route('/search_company', type='json', methods=["POST"], auth="api_key")
    def search_company(self, **kwargs):
        search_term = (kwargs.get("search_term")).strip()
        if search_term:
            auth_api_key = request.auth_api_key_name
            search_term = search_term.replace("http://", "")
            search_term = search_term.replace("https://", "")
            search_term = search_term.replace("www.", "")

            company = request.env['res.partner'].search(['&',
                                                         ('is_company', '=', True),
                                                         '&',
                                                         ('referred', '=', auth_api_key),
                                                         '&',
                                                         ('created_externally', '=', True),
                                                         '|',
                                                         ('name', '=', search_term),
                                                         '|',
                                                         ('lp_domain', '=', search_term),
                                                         '|',
                                                         ('email', '=like', '%' + search_term),
                                                         ('phone', '=', search_term),
                                                         ], limit=1)

            if company:
                return {"company": {"name": company.name, "id": company.id, "country": company.country_id.name,
                                    "industry": company.industry_id.name, "email": company.email,
                                    "phone": company.phone, "mobile": company.mobile,
                                    "domain": company.lp_domain}, "status_code": 200}
            else:
                return {"status_code": 400, "failure_message": "company is not exist."}

        else:
            return {"status_code": 400, "failure_message": " field search_term is not provided from your side"}
