from odoo import fields, models, api 

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_do_sold(self):
        for record in self:
            self.env["account.move"].create({
                'partner_id': record.buyer_id.id,
                'name': record.name,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    (
                        0,
                        0,
                        {
                            'name': record.name,
                            'quantity': 1,
                            'price_unit': record.selling_price,
                        }
                    ),
                    (
                        0,
                        0,
                        {
                            'name': "commission",
                            'quantity': 1,
                            'price_unit': record.selling_price * 0.06,
                        }
                    ),
                    (
                        0,
                        0,
                        {
                            'name': "Additional Fee",
                            'quantity': 1,
                            'price_unit': 100,
                        }
                    )
                ]
            })
        return super().action_do_sold()