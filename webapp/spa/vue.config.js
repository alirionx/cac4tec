module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        //pathRewrite: {'^/api' : ''}
      },
      '/pics': {
        target: 'http://localhost:5000',
        //pathRewrite: {'^/api' : ''}
      }
    }
  }
};