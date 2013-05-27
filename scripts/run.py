#!/usr/bin/env python

from penumbra import app, db

db.create_all()

app.run(debug=True)
