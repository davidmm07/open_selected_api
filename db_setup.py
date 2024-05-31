#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from app import db


if __name__ == '__main__':
    db.create_all()
    db.session.commit()
