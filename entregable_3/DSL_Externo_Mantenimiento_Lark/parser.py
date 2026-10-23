from lark import Lark, Transformer, v_args
from DSL import data


# ============================================================
# GRAMÁTICA
# ============================================================

grammar = r"""
start: (add | update | delete)+

?add: "AGREGAR" add_type_commands "FIN"
?add_type_commands: add_product_commands | add_offer_commands


add_product_commands: "PRODUCTO" int add_product_command_list
add_product_command_list: name price category?
                        | price name category?
                        | name category price
                        | price category name
                        | category name price
                        | category price name

                        
add_offer_commands: "PROMOCION" int add_offer_command_list
add_offer_command_list: name discount conditions
                        | discount name conditions
                        | name conditions discount
                        | discount conditions name
                        | conditions name discount
                        | conditions discount name


?update: "ACTUALIZAR" update_type_commands "FIN"
?update_type_commands: update_product_commands | update_offer_commands


update_product_commands: "PRODUCTO" int update_product_command_list
update_product_command_list: name price? category?
                            | name category? price?
                            | price name? category?
                            | price category? name?
                            | category name? price?
                            | category price? name?

                            
update_offer_commands: "PROMOCION" int update_offer_command_list
update_offer_command_list: name discount? conditions?
                        | name conditions? discount?
                        | discount name? conditions?
                        | discount conditions? name?
                        | conditions name? discount?
                        | conditions discount? name?

                        
?delete: "ELIMINAR PRODUCTO" int -> delete_product
        | "ELIMINAR PROMOCION" int -> delete_offer

conditions: "CUANDO" product_discount_list
product_discount_list: producto+
producto: "PRODUCTO" int quantity?
quantity: "CANTIDAD" operator int

name: "NOMBRE" text
price: "PRECIO" decimal
category: "CATEGORIA" text
discount: "DESCUENTO" decimal

decimal: /[0-9]+(\.[0-9]{1,2})?/
int: /[0-9]+/
text: /"[^"\s]([^"\n]*[^"\s])?"/
operator: "=" -> eq
        | ">=" -> ge

%import common.WS
%ignore WS
"""


# ============================================================
# PARSEA EL DSL
# ============================================================

@v_args(inline=True)
class MantenimientoTransformer(Transformer):
    def int(self, token):
        return int(token)

    def decimal(self, token):
        return float(token)

    def text(self, token):
        return token[1:-1]

    def price(self, token):
        return ("price", token)

    def name(self, token):
        return ("name", token)

    def category(self, token):
        return ("category", token)

    def discount(self, token):
        return ("discount", token)
    
    def delete_product(self, token):
        return ("delete_product", token)

    def add_product_command_list(self, *properties):
            return dict(properties)

    def eq(self):
        return "="

    def ge(self):
        return ">="

    def quantity(self, operator, quantity):
        return { "operator": operator, "quantity": quantity}
    
    def update_product_command_list(self, *properties):
        return dict(properties)

    def delete_offer(self, token):
        return ("delete_offer", token)

    def add_product_commands(self, codigo, campos):
        return ("add_product", codigo, campos)

    def update_product_commands(self, codigo, campos):
        return ("update_product", codigo, campos)


parser = Lark(grammar, start="start", parser="lalr", transformer=MantenimientoTransformer())
tree = parser.parse(data)

from pprint import pprint
print(tree.pretty())