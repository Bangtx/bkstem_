// describe('Master box type page', () => {
//   const boxtype = [
//     {
//       name: 'first box type name',
//       name_eng: 'test',
//       yomi: 'first box type name',
//       bundle_size: 9,
//       id: 1,
//       order_num: 1,
//       search_str: 'first box type nameサイズyomi first test',
//       active: true,
//       created_at: '2021-07-06',
//       created_by: null
//     },
//     {
//       name: 'second box type name',
//       name_eng: 'name eng',
//       yomi: 'second box type name',
//       bundle_size: 9,
//       id: 2,
//       order_num: 2,
//       search_str: 'second boxtype name box l yomi second name eng',
//       active: true,
//       created_at: '2021-07-06',
//       created_by: null
//     }
//   ]

//   const newBoxtype = {
//     name: 'third box type name',
//     name_eng: 'name eng',
//     yomi: 'third box type name',
//     bundle_size: 9,
//     id: 3,
//     order_num: 3,
//     search_str: 'third box type name',
//     active: true,
//     created_at: '2021-07-06',
//     created_by: null
//   }

//   const newBoxTypeNameEmpty = {
//     name: '    ',
//     name_eng: 'name eng',
//     yomi: '',
//     bundle_size: 9,
//     id: 4,
//     order_num: 4,
//     search_str: 'boxtype with name empty',
//     active: true,
//     created_at: '2021-07-06',
//     created_by: null
//   }

//   const updateBoxtype = {
//     name: 'first box type name edit',
//     name_eng: 'test edit',
//     yomi: 'first box type name edit',
//     bundle_size: 9,
//     id: 1,
//     order_num: 1,
//     search_str: 'first box type name editサイズyomi first edit test edit',
//     active: true,
//     created_at: '2021-07-06',
//     created_by: null
//   }

//   // const order = [
//   //   {
//   //     id: 1,
//   //     order_num: 1
//   //   },
//   //   {
//   //     id: 2,
//   //     order_num: 2
//   //   }
//   // ]

//   beforeEach(() => {
//     cy.server()
//     cy.route('/boxtype', boxtype).as('getBoxtype')

//     cy.route({
//       method: 'POST',
//       url: '/boxtype',
//       response: newBoxtype,
//       status: 200
//     }).as('addBoxtype')

//     cy.route({
//       method: 'PUT',
//       url: `/boxtype/${updateBoxtype.id}`,
//       response: updateBoxtype,
//       status: 200
//     }).as('editBoxtype')

//     cy.route(`/common/get-pronunciation?text=${newBoxtype.name}`, newBoxtype.name)
//   })

//   it('should display list size', () => {
//     cy.visit('/master/boxtype')
//     cy.wait('@getBoxtype')

//     cy.get('.v-list-item > span').should(($span) => {
//       expect($span).to.have.length(2)
//       expect($span.eq(0)).to.contain('first box type name')
//       expect($span.eq(1)).to.contain('second box type name')
//     })
//   })

//   it('should display search boxtype by name', () => {
//     cy.get('input').should('exist').type('first')
//     cy.get('.v-list-item > span').should('have.length', 1).should('contain', 'first box type name')

//     cy.get('input').should('exist').clear()
//     cy.get('.v-list-item > span').should('exist').should('have.length', 2)
//     cy.get('.v-list-item > span').should('exist').should('have.length', 2)

//     cy.get('input').should('exist').type('second')
//     cy.get('.v-list-item > span').should('exist').should('contain', 'second box type name')

//     cy.get('input').clear()
//   })

//   it('should display search box type by yomi', () => {
//     cy.get('input').should('exist').type('yomi second')
//     cy.get('.v-list-item > span').should('have.length', 1).should('contain', 'second box type name')

//     cy.get('input').clear()
//     cy.get('.v-list-item > span').should('have.length', 2)

//     cy.get('input').should('exist').type('yomi first')
//     cy.get('.v-list-item > span').should('have.length', 1).should('contain', 'first box type name')
//     // cy.get('.v-list-item > span').should('have.length', 1)
//     cy.get('input').clear()
//   })

//   it('should display search box type by name eng', () => {
//     cy.get('input').should('exist').type('test')
//     cy.get('.v-list-item > span').should('have.length', 1).should('contain', 'first box type name')

//     cy.get('input').clear()
//     cy.get('.v-list-item > span').should('have.length', 2)

//     cy.get('input').should('exist').type('name eng')
//     cy.get('.v-list-item > span').should('have.length', 1).should('contain', 'second box type name')
//     // cy.get('.v-list-item > span').should('have.length', 1)
//     cy.get('input').clear()
//   })

//   it('should show box type information', () => {
//     cy.get('.v-list-item span').eq(0).click()
//     cy.get('.v-input__slot input').eq(1).should('exist').should('contain.value', 'first box type name')
//     cy.get('.v-input__slot input').eq(2).should('exist').should('contain.value', 'first box type name')
//     cy.get('.v-input__slot input').eq(3).should('exist').should('contain.value', 'test')
//     cy.get('.v-input__slot input').eq(4).should('exist').should('contain.value', 9)
//     cy.get('.v-toolbar__items button').click()
//   })

//   it('should edit box type', () => {
//     cy.get('.v-list-item span').eq(0).click()
//     cy.get('.v-input__slot input').eq(1).should('exist').clear()
//     cy.get('.v-input__slot input').eq(1).should('exist').type(updateBoxtype.name)
//     cy.get('.v-input__slot input').eq(2).should('exist').clear()
//     cy.get('.v-input__slot input').eq(2).should('exist').type(updateBoxtype.yomi)
//     cy.get('.v-input__slot input').eq(3).should('exist').clear()
//     cy.get('.v-input__slot input').eq(3).should('exist').type(updateBoxtype.name_eng)
//     cy.get('.v-input__slot input').eq(4).should('exist').clear()
//     cy.get('.v-input__slot input').eq(4).should('exist').type(updateBoxtype.bundle_size)
//     boxtype[0] = updateBoxtype
//     console.log(boxtype)
//     cy.get('.row.ma-1.justify-center button').eq(1).contains('Save').click()
//     cy.get('.v-list-item span').eq(0).click()
//     cy.get('.v-input__slot input').eq(1).should('exist').should('contain.value', updateBoxtype.name)
//     cy.wait(300)
//     // cy.get('.v-input__slot input').eq(2).should('exist').should('contain.value', updateBoxtype.yomi)
//     cy.get('.v-input__slot input').eq(3).should('exist').should('contain.value', updateBoxtype.name_eng)
//     cy.get('.v-input__slot input').eq(4).should('exist').should('contain.value', updateBoxtype.bundle_size)
//     cy.get('.v-toolbar__items button').click()
//     cy.get('.Vue-Toastification__toast-body').should('exist').should('contain.text', 'Update successfully')
//   })

//   it('add new box type', () => {
//     cy.get(
//       '.v-btn.v-btn--is-elevated.v-btn--fab.v-btn--has-bg.v-btn--round.theme--dark.v-size--default.white'
//     ).click()
//     cy.get('.v-icon.notranslate.mdi.mdi-plus.theme--dark').click()
//     cy.get('.v-text-field__slot input').eq(1).should('exist').type(newBoxtype.name)

//     cy.get('.v-text-field__slot input').eq(3).should('exist').type(newBoxtype.name_eng)
//     cy.get('.v-text-field__slot input').eq(4).should('exist').type(newBoxtype.bundle_size)
//     cy.get('.v-card.v-sheet.theme--light button').eq(1).click()

//     boxtype.push(newBoxtype)
//     cy.route({
//       method: 'POST',
//       url: '/boxtype',
//       response: newBoxtype,
//       status: 200
//     })
//   })

//   it('add new witt name exists', () => {
//     cy.get(
//       '.actions-button.v-speed-dial.v-speed-dial--right.v-speed-dial--bottom.v-speed-dial--fixed.v-speed-dial--direction-top'
//     ).click({force: true})
//     cy.get(
//       '.v-icon.notranslate.mdi.mdi-plus.theme--dark'
//     ).click({force: true})
//     cy.get('.v-text-field__slot input').eq(1).should('exist').type(newBoxtype.name)

//     cy.get('.v-text-field__slot input').eq(3).should('exist').type(newBoxtype.name_eng)
//     cy.get('.v-text-field__slot input').eq(4).should('exist').type(newBoxtype.bundle_size)
//     cy.route({
//       method: 'POST',
//       url: `/boxtype`,
//       status: 400,
//       response: { messages: ['Name is already existed'] }
//     })
//     cy.get('.v-card.v-sheet.theme--light button').eq(1).click()
//   })

//   it('add new with name empty', () => {
//     cy.get(
//       '.actions-button.v-speed-dial.v-speed-dial--right.v-speed-dial--bottom.v-speed-dial--fixed.v-speed-dial--direction-top'
//     ).click({force: true})
//     cy.get(
//       '.v-icon.notranslate.mdi.mdi-plus.theme--dark'
//     ).click({force: true})
//     cy.get('.v-text-field__slot input').eq(1).should('exist').type(newBoxTypeNameEmpty.name)

//     cy.get('.v-text-field__slot input').eq(3).should('exist').type(newBoxTypeNameEmpty.name_eng)
//     cy.get('.v-text-field__slot input').eq(4).should('exist').type(newBoxTypeNameEmpty.bundle_size)

//     cy.get('.v-card.v-sheet.theme--light button').eq(1).click({force: true})

//     cy.get('.Vue-Toastification__toast-body').should('exist').should('contain.text', 'Can not save, name is empty')
//   })

//   it('cancel sort box type', () => {
//     cy.get(
//       '.actions-button.v-speed-dial.v-speed-dial--right.v-speed-dial--bottom.v-speed-dial--fixed.v-speed-dial--direction-top'
//     ).click({force: true})
//     cy.get('.v-speed-dial__list button').eq(0).should('exist').click({force: true})
//     cy.get('.v-btn.v-btn--block.v-btn--has-bg.theme--light.elevation-0.v-size--default.white')
//       .eq(0)
//       .click({force: true})
//     cy.get(
//       '.pa-0.button-header.v-btn.v-btn--icon.v-btn--round.theme--dark.v-size--default.white--text'
//     )
//       .eq(1)
//       .should('exist')
//       .click({ force: true })
//   })

//   it('save sort box type', () => {
//     cy.get('.v-speed-dial__list button').eq(0).should('exist').click({force: true})
//     cy.get('.v-btn.v-btn--block.v-btn--has-bg.theme--light.elevation-0.v-size--default.white')
//       .eq(0)
//       .click({force: true})
//     cy.get(
//       '.pa-0.button-header.v-btn.v-btn--icon.v-btn--round.theme--dark.v-size--default.white--text'
//     )
//       .eq(2)
//       .should('exist')
//       .click({ force: true })
//   })

//   it('delete box type', () => {
//     cy.get('.v-list-item span').eq(4).click({force: true})
//     cy.get('.row.ma-1.justify-center button').eq(0).click({force: true})
//     cy.get('.mb-1.btn.v-btn.v-btn--has-bg.theme--light.elevation-0.v-size--default').eq(0).click({force: true})

//     cy.get('.v-list-item span').eq(3).click({force: true})
//     cy.get('.row.ma-1.justify-center button').eq(0).click({force: true})
//     cy.get('.mb-1.btn.v-btn.v-btn--has-bg.theme--light.elevation-0.v-size--default').eq(1).click({force: true})
//     cy.route({
//       method: 'DELETE',
//       url: `/boxtype/3`,
//       status: 200,
//       response: 2
//     })
//     boxtype.splice(2, 1)
//   })
// })
