from odoo import fields, models

class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = 'Contains different tags that helps us describe more the property like cozy or renovated'
    _order = "name"
    name = fields.Char(required = True)
    color = fields.Integer()
    

    _sql_constraints = [
        ('unique_name_tag', 'unique(name)', 'A property tag name must be unique')
    ]