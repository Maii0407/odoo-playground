from odoo import fields, models

class PropertyOffer(models.Model):
  _name = "estate.property.offer"
  _description = "Estate Property Offers"

  price = fields.Float()
  status = fields.Selection(
    string="Offer Status",
    copy=False,
    selection=[
      ('accepted', 'Accepted'),
      ('refused', 'Refused')
    ]
  )
  partner_id = fields.Many2one("res.partner", string="Partner", required=True)
  property_id = fields.Many2one("estate.property", string="Property", required=True)