from app import create_app, db
from app.models import User, Movie, Tag, Review

app = create_app()

# 命令行上下文（可选）
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Movie': Movie, 'Tag': Tag, 'Review': Review}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
