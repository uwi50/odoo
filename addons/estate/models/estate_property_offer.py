from odoo import api, fields, models, exceptions
from datetime import date
from datetime import timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "contains a list of offers of a property and the status of the way the deal is going through"
    _order = "price"

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one(comodel_name="estate.property", string='Property', required=True)
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='property type id',
        related='property_id.property_type_id',
        store=True,
        )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(string="Deadline", compute="_deadline", inverse="_inverse_deadline")

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0 )',
         'An offer price must be strictly positive')
    ]

    @api.depends('validity')
    def _deadline(self):
        for deadline in self:
            deadline.date_deadline = date.today() + timedelta(days=deadline.validity)

    def _inverse_deadline(self):
        for record in self:
            delta = record.date_deadline - date.today()
            record.validity = delta.days
    
    def action_accept(self):       
        for rec in self:
            if any([x == 'Accepted' for x in rec.property_id.offer_ids.mapped('status')]):
                raise UserError('You can only accept one offer')
            rec.status = 'Accepted'
            rec.property_id.write({
                'buyer_id': rec.partner_id.id,
                'selling_price': rec.price,
            })
            #if rec.status != 'Accepted':
            #    rec.property_id.write({
            #        'selling_price' : False
            #    })            
            #rec.buyer_id = True
            #rec.selling_price = True
            
        return True

    def action_refuse(self):
        for rec in self:
            rec.status = 'Refused'
        return True


    @api.model
    def create(self, values):
        """
            Create a new record for a model ModelName
            @param values: provides a data for new r
            @return: returns a id of new record
        """
        offer_val = self.env['estate.property'].browse(values.get('property_id'))
        best_offer = 0
        prices = offer_val.offer_ids.mapped('price')
        if prices:
            best_offer = max(prices)
        #### to be worked on
        if values.get('price') < best_offer:
            raise UserError('Your offer is lower than an existing offer')
        ####
        offer_val.state = 'Offer Received'
        
        result = super(EstatePropertyOffer, self).create(values)
        
        return result
    