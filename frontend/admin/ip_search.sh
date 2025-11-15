#!/bin/env bash
NEW_IP=$(hostname -I | awk '{print $1}')
sed -i "/Admin server listening/ s|http://[^:]*:|http://$NEW_IP:|" server.js
npm start