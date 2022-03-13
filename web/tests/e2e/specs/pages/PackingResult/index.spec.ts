// import moment from 'moment'
//
// describe('Test for Packing Result list page', () => {
//   interface Summary {
//     boxes: number
//     // eslint-disable-next-line camelcase
//     total_stems: number
//     // eslint-disable-next-line camelcase
//     auction_date: string
//   }
//
//   interface AuctionDate {
//     // eslint-disable-next-line camelcase
//     auction_date: string
//     summary?: Array<Summary>
//   }
//
//   const auctionDates: Array<AuctionDate> = [
//     { auction_date: '2021-06' },
//     { auction_date: '2021-05' }
//   ]
//   const summary1: Array<Summary> = [
//     { boxes: 30, total_stems: 900, auction_date: '2021-06-23' },
//     { boxes: 10, total_stems: 100, auction_date: '2021-06-24' },
//     { boxes: 80, total_stems: 6400, auction_date: '2021-06-29' }
//   ]
//
//   beforeEach(() => {
//     cy.server()
//
//     cy.route({
//       method: 'GET',
//       url: '/packing_results/get_auction_dates',
//       response: auctionDates,
//       status: 200
//     }).as('getAuctionDates')
//
//     cy.route({
//       method: 'GET',
//       url: '/packing_results/get_packing_result_summary?start_date=2021-06-01&end_date=2021-06-30',
//       response: summary1,
//       status: 200
//     }).as('getSummary')
//   })
//
//   it('Display list auction dates if there is any packing result', () => {
//     cy.visit('/packing_result/list')
//
//     cy.wait('@getAuctionDates')
//
//     cy.get('.v-list-group__header > .v-list-item__title > .v-list-item__content').should(
//       ($span) => {
//         expect($span).to.have.length(2)
//         expect($span.eq(0)).to.contain('2021年6月')
//         expect($span.eq(1)).to.contain('2021年5月')
//       }
//     )
//   })
//
//   it('Display packing result summary', () => {
//     auctionDates[0] = { ...auctionDates[0], summary: summary1 }
//
//     cy.get('.v-list-item__title > .v-list-item__content').eq(0).click()
//     cy.wait('@getSummary')
//
//     cy.get('.v-list-group__items > .date > .v-list-item').should(($span) => {
//       expect($span).to.have.length(3)
//       // eslint-disable-next-line no-plusplus
//       for (let i = 0; i < $span.length; i++) {
//         expect($span.eq(i)).to.contain(
//           moment(auctionDates[0].summary[i].auction_date).format('YYYY年MM月DD日')
//         )
//         expect($span.eq(i)).to.contain(`箱数: ${auctionDates[0].summary[i].boxes}`)
//         expect($span.eq(i)).to.contain(`合計数: ${auctionDates[0].summary[i].total_stems}`)
//       }
//     })
//   })
// })
//
// describe('Test for Packing Result by date page', () => {
//   it('Does not do much!', () => {
//     expect(true).to.equal(false)
//   })
// })
//
// describe('Test for Packing Result detail page', () => {
//   it('Does not do much!', () => {
//     expect(true).to.equal(true)
//   })
// })
