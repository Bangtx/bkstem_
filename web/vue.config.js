module.exports = {
  transpileDependencies: ['vuetify'],
  pwa: {
    workboxOptions: {
      skipWaiting: true
    }
  },
  devServer: {
    compress: true,
    disableHostCheck: true // That solved it
  }
}
