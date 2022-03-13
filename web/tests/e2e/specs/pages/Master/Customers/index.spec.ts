describe('Master customer page', () => {
  const customers = [
    {
      name: 'first customer name',
      short_name: 'test',
      yomi: 'yomi 1',
      tel: '1231',
      fax: 'fax 1',
      email: 'email 1',
      code: 'code 1',
      id: 1,
      order_num: 1,
      search_str: 'first customer nameサイズtest yomi 1 1231 fax 1 email 1 code 1',
      active: true,
      created_at: '2021-05-26',
      created_by: null
    },
    {
      name: 'second customer name',
      short_name: 'name eng',
      yomi: 'yomi 2',
      tel: '123',
      email: null,
      fax: null,
      code: null,
      id: 2,
      order_num: 2,
      search_str: 'second customer name box l',
      active: true,
      created_at: '2021-05-26',
      created_by: null
    }
  ]

  const newCustomer = {
    name: 'third customer name',
    short_name: 'name eng',
    yomi: 'yomi',
    tel: '123',
    fax: 'fax',
    email: 'email',
    code: 'code',
    id: 3,
    order_num: 3,
    search_str: 'third customer name',
    active: true,
    created_at: '2021-05-26',
    created_by: null
  }

  // const newCustomerNameEmpty = {
  //   name: '    ',
  //   short_name: 'name eng',
  //   yomi: '',
  //   tel: '123',
  //   fax: '',
  //   email: '',
  //   code: '',
  //   id: 4,
  //   order_num: 4,
  //   search_str: 'customer with name empty',
  //   active: true,
  //   created_at: '2021-05-28',
  //   created_by: null
  // }

  // const newCustomerTelEmpty = {
  //   name: 'name',
  //   short_name: 'name eng',
  //   yomi: 'yomi',
  //   tel: '  ',
  //   fax: '',
  //   email: '',
  //   code: '',
  //   id: 4,
  //   order_num: 4,
  //   search_str: 'customer with name empty',
  //   active: true,
  //   created_at: '2021-05-28',
  //   created_by: null
  // }

  // const updateCustomer = {
  //   name: 'third customer name update',
  //   yomi: 'yomi update',
  //   short_name: 'name eng update',
  //   tel: '123',
  //   fax: 'fax',
  //   code: 'code',
  //   email: 'email',
  //   id: 3,
  //   order_num: 3,
  //   search_str: 'third customer name',
  //   active: true,
  //   created_at: '2021-05-26',
  //   created_by: null
  // }

  // const order = [
  //   {
  //     id: 1,
  //     order_num: 1
  //   },
  //   {
  //     id: 2,
  //     order_num: 2
  //   }
  // ]

  beforeEach(() => {
    cy.intercept('GET', '/customers', { body: customers, statusCode: 200 }).as('getCustomers')

    cy.intercept('POST', '/customers', {
      body: newCustomer,
      statusCode: 200
    }).as('createCustomer')

    cy.intercept('PUT', `/customers/${newCustomer.id}`, { body: newCustomer, statusCode: 200 }).as(
      'updateCustomer'
    )

    cy.intercept('DELETE', `/customers/${newCustomer.id}`, {
      body: newCustomer.id,
      statusCode: 200
    })

    cy.intercept('POST', `/customers/sort`, {
      statusCode: 200,
      body: { detail: 'Sort Customer' }
    }).as('sortCustomer')

    cy.intercept(
      {
        pathname: '/common/get-pronunciation',
        query: {
          text: newCustomer.name
        }
      },
      { statusCode: 200, body: newCustomer.name }
    ).as('toYomi')
  })

  it('should display list customer', () => {
    cy.visit('/master/customers')
    cy.wait('@getCustomers')

    cy.get('.v-list-item > span').should(($span) => {
      expect($span).to.have.length(2)
      expect($span.eq(0)).to.contain('first customer name')
      expect($span.eq(1)).to.contain('second customer name')
    })
  })

  it('should display search customer by name', () => {
    cy.get('input').should('exist').type('first')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first customer name')

    cy.get('input').should('exist').clear()
    cy.get('.v-list-item > span').should('length', 2)

    cy.get('input').should('exist').type('second')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'second customer name')
  })

  it('should search customer by yomi', () => {
    cy.get('input').should('exist').clear().type('yomi 1')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first customer name')
  })

  it('should search customer by phone number', () => {
    cy.get('input').should('exist').clear().type('1231')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first customer name')
  })

  it('should search customer by email', () => {
    cy.get('input').should('exist').clear().type('email 1')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first customer name')
  })

  it('should search customer by fax', () => {
    cy.get('input').should('exist').clear().type('fax 1')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first customer name')
  })

  it('should search customer by code', () => {
    cy.get('input').should('exist').clear().type('code 1')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first customer name')
  })

  it('should search customer by short name', () => {
    cy.get('input').should('exist').clear().type('test')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first customer name')
  })

  it('should search customer with upper characters', () => {
    cy.get('input').should('exist').clear().type('BOX L')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'second customer name')
  })

  it('should search customer by half width', () => {
    cy.get('input').should('exist').clear().type('ｻｲｽﾞ')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first customer name')
  })

  it('should search customer render empty', () => {
    cy.get('input').should('exist').type('abcxyz')
    cy.get('.v-list-item > span').should('length', 0)
    cy.get('input').should('exist').clear()
  })

  it('should display customer information', () => {
    cy.get('.v-list-item > span').first().click()
    cy.get('.v-dialog input:first').should('have.value', 'code 1')
    cy.get('.v-dialog input').eq(1).should('have.value', 'first customer name')
    cy.get('.v-dialog input').eq(2).should('have.value', 'yomi 1')
    cy.get('.v-dialog input').eq(3).should('have.value', 'test')
    cy.get('.v-dialog input').eq(4).should('have.value', '1231')
    cy.get('.v-dialog input').eq(5).should('have.value', 'fax 1')
    cy.get('.v-dialog input').eq(6).should('have.value', 'email 1')
    cy.get('i.mdi-close').click()
  })

  //   it('should success create new customer', () => {
  //     cy.wait(500)
  //     cy.get('i.mdi-dots-vertical').click()
  //     cy.get('i.mdi-plus').click()
  //     cy.get('.v-dialog input').eq(1).type(newCustomer.name)
  //     cy.wait(300)
  //     cy.get('.v-dialog input').eq(4).type(newCustomer.tel)
  //
  //     cy.intercept('GET', '/customers', { body: [...customers, newCustomer], statusCode: 200 })
  //     cy.get('span.v-btn__content').contains('Save').click()
  //     cy.wait('@createCustomer').its('request.body').should('contain', {
  //       code: null,
  //       email: null,
  //       fax: null,
  //       name: newCustomer.name,
  //       short_name: null,
  //       tel: newCustomer.tel,
  //       yomi: newCustomer.name
  //     })
  //     cy.get('button.Vue-Toastification__close-button').click()
  //     cy.get('.v-list-item > span').should('length', 3)
  //     cy.get('.v-list-item > span').eq(2).should('contain', 'third customer name')
  //     cy.get('i.mdi-close').click()
  //   })
  //
  //   it('should fail create new customer when name empty', () => {
  //     cy.get('i.mdi-dots-vertical').click()
  //     cy.get('i.mdi-plus').click()
  //     cy.get('.v-dialog input').eq(1).type(newCustomerNameEmpty.name)
  //     cy.get('.v-dialog input').eq(4).type(newCustomerNameEmpty.tel)
  //     cy.get('span.v-btn__content').contains('Save').click()
  //     cy.get('.v-dialog input').eq(1).should('be.empty')
  //     cy.get('.v-list-item > span').should('length', 3)
  //     cy.get('i.mdi-close').click()
  //   })
  //
  //   it('should fail create new customer when tel empty', () => {
  //     cy.get('i.mdi-dots-vertical').click()
  //     cy.get('i.mdi-plus').click()
  //     cy.get('.v-dialog input').eq(1).type(newCustomerTelEmpty.name)
  //     cy.get('.v-dialog input').eq(4).type(newCustomerTelEmpty.tel)
  //     cy.get('span.v-btn__content').contains('Save').click()
  //     cy.get('.v-dialog input').eq(1).should('be.empty')
  //     cy.get('i.mdi-close').click()
  //     cy.get('.v-list-item > span').should('length', 3)
  //   })
  //
  //   it('should fail create new customer when name exits', () => {
  //     cy.wait(500)
  //     cy.get('i.mdi-dots-vertical').click()
  //     cy.get('i.mdi-plus').click()
  //     cy.get('.v-dialog input').eq(1).type(newCustomer.name)
  //     cy.get('.v-dialog input').eq(4).clear().type(newCustomer.tel)
  //
  //     cy.intercept('POST', '/customers', {
  //       body: { messages: ['Name is already existed'] },
  //       statusCode: 400
  //     })
  //     cy.get('span.v-btn__content').contains('Save').click()
  //     cy.get('div.Vue-Toastification__toast-body').should('contain', 'Name is already existed')
  //     cy.wait(500)
  //     cy.get('button.Vue-Toastification__close-button').click()
  //     cy.get('i.mdi-close').click()
  //     cy.get('.v-list-item > span').should('length', 3)
  //   })
  //
  //   it('should success update customer', () => {
  //     cy.get('.v-list-item > span').eq(2).click()
  //     cy.get('.v-dialog input:first').clear().type(updateCustomer.code)
  //     cy.get('.v-dialog input').eq(1).clear().type(updateCustomer.name)
  //     cy.get('.v-dialog input').eq(2).clear().type(updateCustomer.yomi)
  //     cy.get('.v-dialog input').eq(3).clear().type(updateCustomer.short_name)
  //     cy.get('.v-dialog input').eq(4).clear().type(updateCustomer.tel)
  //     cy.get('.v-dialog input').eq(5).clear().type(updateCustomer.fax)
  //     cy.get('.v-dialog input').eq(6).clear().type(updateCustomer.email)
  //
  //     cy.intercept('GET', '/customers', { body: [...customers, updateCustomer] })
  //     cy.get('span.v-btn__content').contains('Save').click()
  //     cy.get('button.Vue-Toastification__close-button').click()
  //     cy.wait('@updateCustomer').its('request.body').should('deep.equal', {
  //       name: updateCustomer.name,
  //       yomi: updateCustomer.yomi,
  //       short_name: updateCustomer.short_name,
  //       tel: updateCustomer.tel,
  //       fax: updateCustomer.fax,
  //       email: updateCustomer.email,
  //       code: updateCustomer.code
  //     })
  //     cy.get('.v-list-item > span').eq(2).should('contain', updateCustomer.name)
  //   })
  //
  //   it('should fail update customer name exits', () => {
  //     cy.get('.v-list-item > span').eq(2).click()
  //     cy.get('.v-dialog input').eq(1).clear().type(updateCustomer.name)
  //     cy.get('.v-dialog input').eq(3).clear().type(updateCustomer.short_name)
  //     cy.get('.v-dialog input').eq(4).clear().type(updateCustomer.tel)
  //
  //     cy.intercept('PUT', `/customers/${newCustomer.id}`, {
  //       body: { messages: ['Name is already existed'] },
  //       statusCode: 400
  //     })
  //     cy.get('span.v-btn__content').contains('Save').click()
  //     cy.get('div.Vue-Toastification__toast-body').should('contain', 'Name is already existed')
  //     cy.get('button.Vue-Toastification__close-button').click()
  //     cy.get('button.Vue-Toastification__close-button').click()
  //     cy.get('i.mdi-close').click()
  //   })
  //
  //   it('should success delete customer', () => {
  //     cy.get('.v-list-item > span').eq(2).click()
  //     cy.get('span').contains('Delete').click()
  //     cy.get('span.red--text').contains('Delete').click()
  //     cy.get('.v-list-item > span').should('length', 2)
  //   })
  //
  //   it('should fail delete customer when cancel', () => {
  //     cy.get('.v-list-item > span').eq(1).click()
  //     cy.get('.light_red').contains('Delete').click()
  //     cy.get('span.blue--text').contains('キャンセル').click()
  //     cy.get('.v-card__title').contains('Edit customer').should('length', 1)
  //     cy.get('button.Vue-Toastification__close-button').click({ multiple: true })
  //     cy.get('i.v-icon.mdi-close').click()
  //     cy.get('.v-list-item > span').should('length', 2)
  //   })
  //
  //   it('should fail delete customer when it is used in order', () => {
  //     cy.wait(500)
  //     cy.get('.v-list-item > span').eq(1).click()
  //     cy.get('.light_red').contains('Delete').click()
  //
  //     cy.intercept('DELETE', `/customers/${customers[1].id}`, {
  //       body: {
  //         messages: [`Can not delete. This customer is used in Order detail: ID=${customers[1].id}`]
  //       },
  //       statusCode: 400
  //     })
  //     cy.get('span.red--text').contains('Delete').click()
  //     cy.get('.Vue-Toastification__toast-body').contains(
  //       'Can not delete. This customer is used in Order detail: ID=2'
  //     )
  //     cy.get('button.Vue-Toastification__close-button').click({ multiple: true })
  //     cy.get('.v-list-item > span').should('length', 2)
  //     cy.get('i.mdi-close').click()
  //   })
  //
  //   it('should sort by name and show info message, buttons', () => {
  //     cy.wait(1000)
  //     cy.get('i.mdi-dots-vertical').click()
  //     cy.get('i.mdi-sort-ascending').click()
  //     cy.get('.v-bottom-sheet').should('be.visible')
  //     cy.get('span.v-btn__content').contains('Sort ascending by name').click()
  //     cy.get('span').contains('Customer list is sorted').should('be.visible')
  //     cy.get('span').contains('Click [Save] button on the top right to save').should('be.visible')
  //     cy.get('.v-list-item > span').should(($span) => {
  //       expect($span.eq(0)).to.contain('first customer name')
  //       expect($span.eq(1)).to.contain('second customer name')
  //     })
  //     cy.get('i.mdi-close').should('be.visible')
  //     cy.get('i.mdi-content-save').should('be.visible')
  //   })
  //
  //   it('should cancel sort by name and hide info message, buttons', () => {
  //     cy.wait(150)
  //     cy.get('i.mdi-close').first().click()
  //     cy.get('i.mdi-close').should('not.be.visible')
  //     cy.get('i.mdi-content-save').should('not.exist')
  //     cy.get('span').contains('Customer list is sorted').should('not.exist')
  //     cy.get('span').contains('Click [Save] button on the top right to save').should('not.exist')
  //   })
  //
  //   it('should save sort by name order and hide info message, buttons', () => {
  //     cy.get('i.mdi-dots-vertical').click()
  //     cy.get('i.mdi-sort-ascending').click()
  //     cy.get('span.v-btn__content').contains('Sort ascending by name').click()
  //     cy.get('i.mdi-content-save').click()
  //     cy.wait('@sortCustomer').its('request.body').should('deep.equal', order)
  //     cy.get('.Vue-Toastification__toast-body').should('contain', 'Save order successful')
  //     cy.get('button.Vue-Toastification__close-button').click()
  //     cy.get('i.mdi-close').should('not.be.visible')
  //     cy.get('i.mdi-content-save').should('not.exist')
  //     cy.get('span').contains('Customer list is sorted').should('not.exist')
  //     cy.get('span').contains('Click [Save] button on the top right to save').should('not.exist')
  //     cy.get('.v-list-item > span').should(($span) => {
  //       expect($span.eq(0)).to.contain('first customer name')
  //       expect($span.eq(1)).to.contain('second customer name')
  //     })
  //   })
  // })
})
