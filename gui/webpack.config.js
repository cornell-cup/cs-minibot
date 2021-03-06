var path = require('path');
var webpack = require('webpack');

module.exports = {
    entry: './static/js/main.js',
    output: {
        path: path.resolve(__dirname, './static/build'),
        filename: 'app.bundle.js'
    },
    module: {
        loaders: [
            {
                test: /\.js$/,
                loader: 'babel-loader',
                query: {
                    presets: ['es2015', 'react']
                }
            },
            // { 
            //     test: /\.js$/, 
            //     loader: 'eslint-loader', 
            //     exclude: /node_modules/ 
            // },
        ]
    },
    stats: {
        colors: true
    },
    devtool: 'source-map'
};