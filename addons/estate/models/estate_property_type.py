from odoo import api, fields, models, exceptions

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types like House or appartment,..."
    _order = "name"

    name = fields.Char(string="Property Type Name", required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    property_type_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offer id')
    offer_count = fields.Integer(compute="_compute_offers", string='Offers')
    
    @api.depends('offer_ids')
    def _compute_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('unique_name_type', 'unique(name)', 'A property type name must be unique')
    ]
