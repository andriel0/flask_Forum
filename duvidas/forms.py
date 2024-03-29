from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from duvidas.models import Usuario
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed


class FormCriarConta(FlaskForm):
    user = StringField('Nome de Usuário', validators=[DataRequired(), Length(4, 16)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    conf_senha = PasswordField('Confirmação de Senha', validators=[EqualTo('senha')])
    btn_submit_cadastro = SubmitField('Cadastrar')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Já existe outro usuário com esse email, cadastre outro email.')

    def validate_user(self, user):
        usuario = Usuario.query.filter_by(user=user.data).first()
        if usuario:
            raise ValidationError('Nome de usuário existente, cadastre outro nome de usuário.')


class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    check_lembrar = BooleanField('Lembrar dados')
    btn_submit_login = SubmitField('Fazer Login')


class FormVerificar(FlaskForm):
    codigo = StringField('Código de Verificação', validators=[Length(6, 6)])
    btn_submit_verificar = SubmitField('Verificar')


class FormCriarPost(FlaskForm):
    titulo = StringField('Título da Dúvida', validators=[DataRequired(), Length(3, 140)])
    corpo = TextAreaField('Escreva sua dúvida aqui', validators=[DataRequired()])
    btn_submit_criar_post = SubmitField('Publicar')




class FormEditarPerfil(FlaskForm):
    user = StringField('Nome do Usuário', validators=[DataRequired(), Length(5, 20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    senha = PasswordField('Senha')
    conf_senha = PasswordField('Confirmação de Senha', validators=[EqualTo('senha')])
    bio = TextAreaField('Bio', validators=[Length(3,135)])
    btn_submit_editar = SubmitField('Atualizar')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe outro usuário com esse email, cadastre outro email.')

    def validate_user(self, user):
        if current_user.user != user.data:
            usuario = Usuario.query.filter_by(user=user.data).first()
            if usuario:
                raise ValidationError('Nome de usuário existente, altere com outro nome de usuário.')