from odoo import fields, models

class PropertyTag(models.Model):
  _name = "estate.property.tag"
  _description = "Estate Property Tag"

  name = fields.Char(required=True)

  _sql_constraints = [
    (
      'check_name',
      'UNIQUE(name)',
      'Property tag name must be unique'
    )
  ]
