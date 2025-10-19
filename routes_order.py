from fastapi import APIRouter, Depends, HTTPException
from models import Pedido, Usuario, ItemPedido
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema
from sqlalchemy.orm import Session

router_order = APIRouter(prefix="/pedidos", tags=["Pedidos"], dependencies=[Depends(verificar_token)])

@router_order.get("/")
async def pedidos():
    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas de pedidos precisam de autenticação
    """
    return {"mensagem": "Voccê acessou a rota de pedidos"}

@router_order.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem" : f"Pedido criado com sucesso. Id do Pedido: {novo_pedido.id}"}


@router_order.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    # usuario.admin = True
    # usuario.id = pedido.usuario
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificiação")
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido {pedido.id} cancelado com sucesso" ,
        "pedido": pedido
    }
    
@router_order.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
        }

@router_order.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, 
                                item_pedido_schema: ItemPedidoSchema,
                                session: Session = Depends(pegar_sessao),
                                usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação")
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho,
                             item_pedido_schema.preco_unitario, id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": "Item criado com sucesso",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }