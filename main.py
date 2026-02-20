from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from plyer import camera, gps
import os
import bcrypt
import uuid

from supabase_conexao import supabase
from pdf_generator import gerar_pdf


KV = '''
ScreenManager:
    LoginScreen:
    CadastroScreen:
    MenuScreen:
    NovaOcorrenciaScreen:
    ListaOcorrenciasScreen:

<LoginScreen>:
    name: "login"
    MDBoxLayout:
        orientation: "vertical"
        spacing: 20
        padding: 40

        MDLabel:
            text: "Sistema de Ocorrências"
            halign: "center"
            font_style: "H4"

        MDTextField:
            id: usuario
            hint_text: "Usuário"

        MDTextField:
            id: senha
            hint_text: "Senha"
            password: True

        MDRaisedButton:
            text: "Entrar"
            on_release: app.login(usuario.text, senha.text)

        MDRaisedButton:
            text: "Cadastrar Usuário"
            on_release: app.root.current = "cadastro"


<CadastroScreen>:
    name: "cadastro"
    MDBoxLayout:
        orientation: "vertical"
        spacing: 20
        padding: 40

        MDTextField:
            id: novo_usuario
            hint_text: "Novo Usuário"

        MDTextField:
            id: nova_senha
            hint_text: "Nova Senha"
            password: True

        MDRaisedButton:
            text: "Salvar"
            on_release: app.cadastrar_usuario(novo_usuario.text, nova_senha.text)

        MDRaisedButton:
            text: "Voltar"
            on_release: app.root.current = "login"


<MenuScreen>:
    name: "menu"
    MDBoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 20

        MDRaisedButton:
            text: "Nova Ocorrência"
            on_release: app.root.current = "nova"

        MDRaisedButton:
            text: "Ver Ocorrências"
            on_release:
                app.carregar_ocorrencias()
                app.root.current = "lista"

        MDRaisedButton:
            text: "Exportar Relatório PDF"
            on_release: app.exportar_pdf()

        MDRaisedButton:
            text: "Sair"
            on_release: app.root.current = "login"


<NovaOcorrenciaScreen>:
    name: "nova"
    MDBoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 10

        MDTextField:
            id: descricao
            hint_text: "Descrição da ocorrência"

        MDRaisedButton:
            text: "Capturar Foto"
            on_release: app.tirar_foto()

        MDRaisedButton:
            text: "Salvar Ocorrência"
            on_release: app.salvar_ocorrencia(descricao.text)

        MDRaisedButton:
            text: "Voltar"
            on_release: app.root.current = "menu"


<ListaOcorrenciasScreen>:
    name: "lista"
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Ocorrências"
            left_action_items: [["arrow-left", lambda x: setattr(app.root, "current", "menu")]]

        ScrollView:
            MDList:
                id: lista_ocorrencias
'''


class LoginScreen(Screen):
    pass


class CadastroScreen(Screen):
    pass


class MenuScreen(Screen):
    pass


class NovaOcorrenciaScreen(Screen):
    pass


class ListaOcorrenciasScreen(Screen):
    pass


class OcorrenciaApp(MDApp):

    foto_caminho = ""
    usuario_logado = ""
    latitude = ""
    longitude = ""

    def build(self):
        return Builder.load_string(KV)

    # GPS
    def on_start(self):
        try:
            gps.configure(on_location=self.on_location)
            gps.start(minTime=1000, minDistance=0)
        except:
            print("GPS não disponível neste dispositivo")

    def on_location(self, **kwargs):
        self.latitude = str(kwargs.get("lat"))
        self.longitude = str(kwargs.get("lon"))
        print("Localização:", self.latitude, self.longitude)

    # LOGIN
    def login(self, usuario, senha):
        try:
            response = supabase.table("usuarios") \
                .select("*") \
                .eq("usuario", usuario) \
                .execute()

            if response.data:
                senha_hash = response.data[0]["senha"]

                if bcrypt.checkpw(senha.encode(), senha_hash.encode()):
                    self.usuario_logado = usuario
                    self.root.current = "menu"
                else:
                    print("Senha incorreta")
            else:
                print("Usuário não encontrado")

        except Exception as e:
            print("Erro no login:", e)

    # CADASTRO
    def cadastrar_usuario(self, usuario, senha):
        try:
            senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

            supabase.table("usuarios").insert({
                "usuario": usuario,
                "senha": senha_hash,
                "nivel": "usuario",
                "bloqueado": False
            }).execute()

            print("Usuário cadastrado!")
            self.root.current = "login"

        except Exception as e:
            print("Erro ao cadastrar:", e)

    # FOTO
    def tirar_foto(self):
        caminho = os.path.join(os.getcwd(), "foto.jpg")
        self.foto_caminho = caminho
        camera.take_picture(filename=caminho)
        print("Foto salva localmente")

    # SALVAR OCORRÊNCIA
    def salvar_ocorrencia(self, descricao):
        try:
            if not self.foto_caminho:
                print("Tire uma foto primeiro!")
                return

            nome_arquivo = f"{uuid.uuid4()}.jpg"

            with open(self.foto_caminho, "rb") as f:
                supabase.storage.from_("fotos").upload(nome_arquivo, f)

            url_publica = supabase.storage.from_("fotos").get_public_url(nome_arquivo)

            supabase.table("ocorrencias").insert({
                "descricao": descricao,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "foto": url_publica,
                "usuario": self.usuario_logado
            }).execute()

            print("Ocorrência salva com sucesso!")
            self.root.current = "menu"

        except Exception as e:
            print("Erro ao salvar:", e)

    # CARREGAR LISTA
    def carregar_ocorrencias(self):
        try:
            tela = self.root.get_screen("lista")
            lista = tela.ids.lista_ocorrencias
            lista.clear_widgets()

            response = supabase.table("ocorrencias") \
                .select("*") \
                .order("id", desc=True) \
                .execute()

            for item in response.data:
                texto = f"{item['descricao']} - {item['usuario']}"
                lista.add_widget(OneLineListItem(text=texto))

        except Exception as e:
            print("Erro ao carregar:", e)

    def exportar_pdf(self):
        gerar_pdf()
        print("PDF gerado!")


if __name__ == "__main__":
    OcorrenciaApp().run()