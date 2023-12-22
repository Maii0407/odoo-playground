from odoo import fields, models

class PropertyType(models.Model):
  _name = "estate.property.type"
  _description = "Estate Property Type"

  name = fields.Char(required=True)

  _sql_constraints = [
    (
      'check_name',
      'UNIQUE(name)',
      'Property Type name must be unique'
    )
  ]
