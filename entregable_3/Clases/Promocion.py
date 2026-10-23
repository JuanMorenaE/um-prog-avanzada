from Clases.Condicion import Condicion

class Promocion:
    def __init__(self, codigo):
        self.codigo = codigo
        self.nombre = None
        self.descuento = None
        self.condiciones = []

    def agregar_condicion(self, producto):
        if any(condicion.producto.codigo == producto.codigo for condicion in self.condiciones):
            raise ValueError(f"La promocion {self.codigo} ya tiene una condicion para el producto {producto.codigo}")

        condicion = Condicion(producto)
        self.condiciones.append(condicion)
        return condicion

    def validar(self):
        if not isinstance(self.codigo, int):
            raise ValueError(f"El codigo de promocion debe ser un entero (recibido: {self.codigo})")
        if not isinstance(self.nombre, str):
            raise ValueError(f"La promocion {self.codigo} debe tener un nombre de tipo texto")
        if not isinstance(self.descuento, (int, float)) or not 0 < self.descuento <= 100:
            raise ValueError(f"La promocion {self.codigo} debe tener un descuento entre 0 y 100 (recibido: {self.descuento})")
        if not self.condiciones:
            raise ValueError(f"La promocion {self.codigo} debe tener al menos una condicion")

        for condicion in self.condiciones:
            condicion.validar()

    def __str__(self):
        text = f"{self.codigo}. {self.nombre} - {self.descuento}% OFF"

        for condicion in self.condiciones:
            text += f"\n\t- {condicion}"

        return text



Tree(
    Token('RULE', 'start'), [
        Tree(
            Token('RULE', 'add'), [
                Tree(
                    Token('RULE', 'add_type_commands'), [
                        Tree(
                            Token('RULE', 'add_product_commands'),[
                                5, 
                                Tree(
                                    Token('RULE', 'add_product_command_list'), [
                                        Tree(
                                            Token('RULE', 'name'), [
                                                Tree(
                                                    Token('RULE', 'text'), [
                                                        Token('__ANON_4', '"Azúcar"')
                                                    ]
                                                )
                                            ]
                                        ), 
                                        Tree(
                                            Token('RULE', 'price'), [Tree(Token('RULE', 'decimal'), [Token('__ANON_2', '60')])]), Tree(Token('RULE', 'category'), [Tree(Token('RULE', 'text'), [Token('__ANON_4', '"Comestible"')])])])])])]), Tree(Token('RULE', 'add'), [Tree(Token('RULE', 'add_type_commands'), [Tree(Token('RULE', 'add_product_commands'), [6, Tree(Token('RULE', 'add_product_command_list'), [Tree(Token('RULE', 'price'), [Tree(Token('RULE', 'decimal'), [Token('__ANON_2', '45')])]), Tree(Token('RULE', 'name'), [Tree(Token('RULE', 'text'), [Token('__ANON_4', '"Leche"')])])])])])]), Tree(Token('RULE', 'update'), [Tree(Token('RULE', 'update_type_commands'), [Tree(Token('RULE', 'update_product_commands'), [3, Tree(Token('RULE', 'update_product_command_list'), [Tree(Token('RULE', 'name'), [Tree(Token('RULE', 'text'), [Token('__ANON_4', '"Coca Cola"')])])])])])]), Tree(Token('RULE', 'update'), [Tree(Token('RULE', 'update_type_commands'), [Tree(Token('RULE', 'update_product_commands'), [2, Tree(Token('RULE', 'update_product_command_list'), [Tree(Token('RULE', 'category'), [Tree(Token('RULE', 'text'), [Token('__ANON_4', '"Comestible"')])]), Tree(Token('RULE', 'price'),[Tree(Token('RULE', 'decimal'), [Token('__ANON_2', '35.5')])])])])])]), Tree(Token('RULE', 'update'), [Tree(Token('RULE', 'update_type_commands'), [Tree(Token('RULE', 'update_offer_commands'), [1, Tree(Token('RULE', 'update_offer_command_list'), [Tree(Token('RULE', 'conditions'), [Tree(Token('RULE', 'product_discount_list'), [2, Tree(Token('RULE', 'quantity'), [Tree('ge', []), 3])])]), Tree(Token('RULE', 'name'), [Tree(Token('RULE', 'text'), [Token('__ANON_4', '"Harina x3"')])])])])])]), Tree(Token('RULE', 'add'), [Tree(Token('RULE', 'add_type_commands'), [Tree(Token('RULE', 'add_offer_commands'), [3, Tree(Token('RULE', 'add_offer_command_list'), [Tree(Token('RULE', 'discount'), [Tree(Token('RULE', 'decimal'),[Token('__ANON_2', '30.5')])]), Tree(Token('RULE', 'name'), [Tree(Token('RULE', 'text'), [Token('__ANON_4', '"Leche + Azúcar"')])]), Tree(Token('RULE', 'conditions'), [Tree(Token('RULE', 'product_discount_list'), [6, 5, Tree(Token('RULE', 'quantity'), [Tree('eq', []), 1])])])])])])]), Tree('delete_product', [1]), Tree('delete_offer', [2])])