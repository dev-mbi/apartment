from app import create_app
app = create_app()
print(f'Routes: {len(list(app.url_map.iter_rules()))}')
print('App started OK')
