var path      = require('path');
var APP_DIR   = path.resolve(__dirname, './'); // input
var BUILD_DIR = path.resolve(__dirname, './javascripts/dist'); // output

var config = {
  // for now generate one compiled js file per entry point / html page
  entry: {
    'css-theme': APP_DIR + '/javascripts/css-theme.js',
    dashboard: APP_DIR + '/javascripts/dashboard.js',
    explore: APP_DIR + '/javascripts/explore.js',
    featured: APP_DIR + '/javascripts/featured.js',
    sql: APP_DIR + '/javascripts/sql.js',
    standalone: APP_DIR + '/javascripts/standalone.js'
  },
  output: {
    path: BUILD_DIR,
    filename: '[name].entry.js'
  },
  module: {
    loaders: [
      {
        test: /\.jsx?/,
        include: APP_DIR,
        exclude: APP_DIR + '/node_modules',
        loader: 'babel'
      },
    /* for require('*.css') */
      {
        test: /\.css$/,
        include: APP_DIR,
        loader: "style-loader!css-loader"
      },
    /* for css linking images */
      { test: /\.png$/, loader: "url-loader?limit=100000" },
      { test: /\.jpg$/, loader: "file-loader" },
      { test: /\.gif$/, loader: "file-loader" },
    /* for font-awesome */
      { test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "url-loader?limit=10000&minetype=application/font-woff" },
      { test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "file-loader" },
    /* for require('*.less') */
      {
        test: /\.less$/,
        include: APP_DIR,
        loader: "style!css!less"
      }
    ]
  },
  plugins: []
};

module.exports = config;
