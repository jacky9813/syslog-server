#!/bin/bash
BASEDIR=$(pwd)
echo "Compiling babel script"
cd $BASEDIR/babel-compile
npm run build
if [ "$?" -ne "0" ]; then
    echo "Error occured when compiling babel script"
    echo "Terminating"
    exit 1
fi
npm run minify
if [ "$?" -ne "0" ]; then
    echo "Error occured when minifying babel script"
    echo "Terminating"
    exit 1
fi

cd $BASEDIR
if [[ $EUID -ne 0 ]]; then
    # Explaining why root access is required
    echo "Building Docker image requires root access, sudoing..."
    sudo docker-compose build
else
    # Already is root
    docker-compose build
fi

echo "Cleaning up"
# Cleaning up babel compiler temporary file
rm $BASEDIR/babel-compile/app.js