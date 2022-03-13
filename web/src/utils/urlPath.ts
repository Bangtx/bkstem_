const START = { path: '/', name: 'Start' }
const HOME = { path: '/home', name: 'home.title' }
const MENU = { path: '/menu', name: 'Menu' }
const ORDER_SUMMARY = { path: '/orders/summary', name: 'order.title' }

const ORDER_BY_AUCTION = { path: '/orders/auction_date/:date', name: 'order.menu_title' }
const ASSIGN = { path: '/assigns', name: 'assign.title' }
const ASSIGN_FORM = { path: '/assigns/detail/:assignId', name: 'assign.create_title' }

const ORDER_FORM = { path: '/orders/form', name: 'create_order.title' }
const ORDER_DETAIL_FORM = {
  path: '/orders/:auctionDate/:orderId/details/:detailId',
  name: 'order.input'
}
const SALES = { path: '/sales', name: 'Sales' }
const SETTING = { path: '/setting', name: 'Setting' }
const LOGIN_CALLBACK = { path: '/account/callback', name: 'Login' }
const MASTER = { path: '/master', name: 'master.title' }
const QUICK_INPUT = { path: '/master/quick_input', name: 'master.quick_input.title' }
const MASTER_SIZES = { path: '/master/sizes', name: 'master.size.title' }
const MASTER_UNITS = { path: '/master/units', name: 'master.unit.title' }
const MASTER_ITEMS = { path: '/master/items', name: 'master.item.title' }
const MASTER_VARIETIES = { path: '/master/varieties', name: 'product' }
const MASTER_CUSTOMERS = { path: '/customers', name: 'master.customer.title' }
const MASTER_QUALITIES = { path: '/master/qualities', name: 'master.quality.title' }
const PACKING_RESULT_LIST = { path: '/packing_result/list', name: 'packing_result.list.title' }
const PACKING_RESULT_DATE = { path: '/packing_result', name: 'packing_result.date.title' }
const BOXTYPE_LIST = { path: '/master/box_type', name: 'master.box_type.title' }
const PACKING_RESULT_DETAIL = {
  path: '/packing_result/detail/:detailId',
  name: 'packing_result.detail.title'
}
const HARVEST_RESULT = {
  path: '/harvest_result',
  name: 'harvest.result.title'
}
const HARVEST_RESULT_FORM = {
  path: '/harvest_result/results/:resultId',
  name: 'harvest.create_screen_title'
}
const AUCTION_DATE_SETTING = {
  path: '/master/auction_date',
  name: 'master.auction_date.title'
}
const ASSIGN_SERI = { path: '/assign_seri/', name: 'assign_seri.title' }
const ASSIGN_ORDER = { path: '/assign_order/', name: 'assign_order.title' }

const DISABLE_NAVIGATION = [
  HOME.path,
  ORDER_SUMMARY.path,
  ASSIGN.path,
  MASTER.path,
  HARVEST_RESULT.path,
  PACKING_RESULT_LIST.path
]

export {
  START,
  HOME,
  MENU,
  ORDER_SUMMARY,
  ORDER_FORM,
  ASSIGN,
  ASSIGN_FORM,
  SALES,
  SETTING,
  DISABLE_NAVIGATION,
  ORDER_BY_AUCTION,
  ORDER_DETAIL_FORM,
  LOGIN_CALLBACK,
  MASTER,
  MASTER_SIZES,
  MASTER_UNITS,
  MASTER_ITEMS,
  MASTER_VARIETIES,
  MASTER_CUSTOMERS,
  MASTER_QUALITIES,
  PACKING_RESULT_LIST,
  PACKING_RESULT_DATE,
  PACKING_RESULT_DETAIL,
  BOXTYPE_LIST,
  QUICK_INPUT,
  HARVEST_RESULT,
  HARVEST_RESULT_FORM,
  AUCTION_DATE_SETTING,
  ASSIGN_SERI,
  ASSIGN_ORDER
}
