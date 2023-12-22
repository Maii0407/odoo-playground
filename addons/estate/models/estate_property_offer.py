from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError

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
  validity = fields.Integer("Validity (days)", default=7)
  date_deadline = fields.Date("Deadline", compute="_compute_date_deadline")

  _sql_constraints = [
    (
      'check_price',
      'CHECK(price > 0)',
      'Offer price must be positive value'
    )
  ]

  @api.depends("validity", "create_date")
  def _compute_date_deadline(self):
    for record in self:
      if record.create_date:
        record.date_deadline = record.create_date + timedelta(days=record.validity)
      else:
        record.date_deadline = fields.Datetime.today() + timedelta(days=record.validity)

  # def _inverse_date_deadline(self):
  #   for record in self:
  #     if record.date_deadline:
  #       record.validity = (record.date_d?eadline - record.create_date).days

  def accept_offer(self):
    for record in self:
      if record.property_id.state == 'offer accepted':
        raise UserError("Another offer has already been accepted for this property.")

      record.status = 'accepted'
      property_id = record.property_id
      property_id.buyer = record.partner_id
      property_id.selling_price = record.price
      property_id.state = 'offer accepted'
    return True
  
  def refuse_offer(self):
    for record in self:
      record.status = 'refused'
    return True
