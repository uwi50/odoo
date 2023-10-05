from odoo import api, fields, models, exceptions
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round



class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property descriptions"
    _order = "id desc"

    
    x = date.today() + relativedelta(months=3)
    name = fields.Char('Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    property_type_id = fields.Many2one(comodel_name='estate.property.type', string='property_type')
    tags_type_ids = fields.Many2many(comodel_name='estate.property.tags', string='Tags')
    salesperson_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    date_availability = fields.Date('Available From', copy=False, default=x)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')],
        help = "Type is used to separate North, South, East and West"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        selection=[('New', 'New'), ('Offer Received', 'Offer Received'), ('Offer Accepted', 'Offer Accepted'), ('Sold', 'Sold'),
                    ('Canceled', 'Canceled')]
    ,default='New', required=True, copy=False)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='offer')
    total_area = fields.Integer(compute="_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_best_price", string="Best Offer")
    #property_type_id = fields.Many2one('estate.property.type')
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0 )',
         'A property expected price must be strictly positive'),
         ('check_selling_price', 'CHECK(selling_price >= 0 )',
         'A property selling price must be positive')
    ]
    
###### To be Worked on #####
    @api.depends('offer_ids.price')
    @api.constrains('expected_price')
    def _check_price(self):
       for record in self:
            if record.offer_ids.price < (0.9 * record.expected_price) and record.offer_ids.price != 0:
                raise ValidationError('The selling price cannot be lower than 90% of the expected price.')
    ######        
    
    @api.depends('garden_area', 'living_area')
    def _total_area(self):
        for area in self:
            area.total_area = area.garden_area + area.living_area

    @api.depends('offer_ids.price')
    def _best_price(self):
        for best in self:
            best_price = 0
            if best.offer_ids:
                best_price = max(best.offer_ids.mapped('price'))
            best.best_price = best_price

    

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area =  10
            self.garden_orientation = "North"
        elif self.garden == False:
            self.garden_area = False
            self.garden_orientation = False

    def action_do_sold(self):
        if self.state == 'New' or  self.state == 'Offer Received' or self.state == 'Offer Accepted' or self.state == 'Sold':
            self.state = 'Sold'
        else:
            raise exceptions.UserError('Sold property cannot be Canceled.')
        return True

    def action_do_cancel(self):
        if self.state == 'New' or self.state == 'Offer Received' or self.state == 'Offer Accepted' or self.state == 'Canceled':
            self.state = 'Canceled'
        else:
            raise exceptions.UserError('Canceled property cannot be Sold.')
        return True

    def unlink(self):
        res = super().unlink()
        for rec in self:
            if rec.state not in ['New', 'Canceled']:
                raise exceptions.UserError("You cannot delete this property")
        return res

   