from .app import app, db
from .forms import *
from .services import *
from .gestion_erreurs import *
from monApp.models import *
from config import TITLE, AUJOURDHUI
from flask import render_template, request, url_for, redirect, session, abort, flash
from flask_login import logout_user, login_user, login_required, current_user
from flask import jsonify
from datetime import datetime
from sqlalchemy import or_
import shutil
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import SignatureExpired















if __name__ == "__main__":
    app.run()
    db.close()