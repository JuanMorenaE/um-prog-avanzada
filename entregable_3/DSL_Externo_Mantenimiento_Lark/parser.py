from lark import Lark, Transformer, v_args
from DSL import data

grammar = r"""
start: add* update* delete*

add: "AGREGAR" add_type_commands "FIN"
add_type_commands: add_product_commands | add_offer_commands


add_product_commands: "PRODUCTO" code add_product_command_list "FIN"
add_product_command_list: name price category?
                        | price name category?
                        | name category price
                        | price category name
                        | category name price
                        | category price name

                        
add_offer_commands: "PROMOCION" code add_offer_command_list "FIN"
add_offer_command_list: name price disscount
                        | price name disscount
                        | name disscount price
                        | price disscount name
                        | disscount price name
                        | disccount name price


update: "ACTUALIZAR" type update_command_list "FIN"
delete: "ELIMINAR" type number


name: "NOMBRE" text
price: "PRECIO" number
category: "CATEGORIA" text
disscount: "DESCUENTO" number
condition: "CUANDO" product_condition_list

product_condition_list: "PRODUCTO" number condition? product_condition_list*
condition: "CANTIDAD" operator number

number: /[1-9]([0-9]+)?(.[0-9]{1,2})/
code: /[0-9]+/
text: /\"[A-Za-z_][A-Za-z0-9_\s]*\"/
operator: "=" | ">="
type: "PRODUCTO" | "PROMOCION"
"""

parser = Lark(grammar, parser="lalr", transformer=SecurityTransformer())
result = parser.parse(data)