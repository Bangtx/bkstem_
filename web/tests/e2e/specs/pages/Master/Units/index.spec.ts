describe('Master unit page', () => {
  const units = [
    {
      name: 'first unit nameサイズ',
      id: 1,
      yomi: 'first unit nameサイズ',
      search_str: 'first unit nameサイズ',
      order_num: 1,
      active: true,
      created_at: '2021-06-01',
      created_by: null
    },
    {
      name: '1second unit name',
      id: 2,
      yomi: '1second unit name',
      search_str: '1second unit name',
      order_num: 2,
      active: true,
      created_at: '2021-06-01',
      created_by: null
    }
  ]

  const newUnit = {
    name: 'third unit name',
    yomi: 'third unit name',
    id: 3,
    order_num: 3,
    search_str: 'third unit name',
    active: true,
    created_at: '2021-06-01',
    created_by: null
  }

  // const newUnitNameEmpty = {
  //   name: '    ',
  //   yomi: '',
  //   id: 4,
  //   order_num: 4,
  //   active: true,
  //   created_at: '2021-06-01',
  //   created_by: null
  // }

  // const updateUnit = {
  //   name: 'third unit name update',
  //   yomi: 'third unit name update',
  //   id: 3,
  //   order_num: 3,
  //   active: true,
  //   created_at: '2021-06-01',
  //   created_by: null
  // }

  // const order = [
  //   {
  //     id: 2,
  //     order_num: 1
  //   },
  //   {
  //     id: 1,
  //     order_num: 2
  //   }
  // ]

  beforeEach(() => {
    cy.intercept('GET', '/units', { body: units }).as('getUnits')

    cy.intercept('POST', '/units', { body: newUnit, statusCode: 200 }).as('createUnit')

    cy.intercept('PUT', `/units/${newUnit.id}`, {
      body: newUnit,
      statusCode: 200
    }).as('updateUnit')

    cy.intercept('DELETE', `/units/${newUnit.id}`, {
      body: newUnit.id,
      statusCode: 200
    })

    cy.intercept('POST', '/units/sort', {
      statusCode: 200,
      response: { detail: 'Sort Size' }
    }).as('sortUnit')

    cy.intercept(
      {
        pathname: '/common/get-pronunciation',
        query: {
          text: newUnit.name
        }
      },
      { statusCode: 200, body: newUnit.name }
    ).as('toYomi')
  })

  it('should display list unit', () => {
    cy.visit('/master/units')
    cy.wait('@getUnits')

    cy.get('.v-list-item > span').should(($span) => {
      expect($span).to.have.length(2)
      expect($span.eq(0)).to.contain('first unit nameサイズ')
      expect($span.eq(1)).to.contain('1second unit name')
    })
  })

  it('should display search unit by name', () => {
    cy.get('input').should('exist').type('first')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first unit nameサイズ')

    cy.get('input').should('exist').clear()
    cy.get('.v-list-item > span').should('length', 2)

    cy.get('input').should('exist').type('second')
    cy.get('.v-list-item > span').should('length', 1).should('contain', '1second unit name')
  })

  it('should search unit with upper characters', () => {
    cy.get('input').should('exist').clear().type('SECOND')
    cy.get('.v-list-item > span').should('length', 1).should('contain', '1second unit name')
  })

  it('should search unit by half width', () => {
    cy.get('input').should('exist').clear().type('ｻｲｽﾞ')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first unit nameサイズ')
  })

  it('should search unit render empty', () => {
    cy.get('input').should('exist').type('abcxyz')
    cy.get('.v-list-item > span').should('length', 0)
    cy.get('span').should('contain', 'There is no unit')
    cy.get('input').should('exist').clear()
    cy.get('.v-list-item > span').should('length', 2)
  })

  it('should display unit information', () => {
    cy.get('.v-list-item > span').first().click()
    cy.get('.v-dialog input').eq(0).should('have.value', 'first unit nameサイズ')
    cy.get('.v-dialog input').eq(1).should('have.value', 'first unit nameサイズ')
    cy.get('i.mdi-close').click()
  })

  // it('should success create new unit', () => {
  //   cy.wait(200)
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-plus').click()
  //   cy.get('.v-dialog input').eq(0).type(newUnit.name)
  //   cy.wait('@toYomi')
  //   cy.intercept('GET', '/units', { body: [...units, newUnit] })
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.wait('@createUnit').its('request.body').should('deep.equal', {
  //     name: newUnit.name,
  //     yomi: newUnit.yomi
  //   })
  //   cy.get('i.mdi-close').first().click()
  //   cy.get('.v-list-item > span').should('length', 3)
  //   cy.get('.v-list-item > span').eq(2).should('contain', 'third unit name')
  // })

  // it('should fail create new unit when name empty', () => {
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-plus').click()
  //   cy.get('.v-dialog input').eq(0).type(newUnitNameEmpty.name)
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('.v-dialog input').eq(0).should('be.empty')
  //   cy.get('.Vue-Toastification__toast-body').should('contain', 'Cannot save, name is empty')
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('i.mdi-close').first().click()
  //   cy.get('.v-list-item > span').should('length', 3)
  // })

  // it('should fail create new unit when name exits', () => {
  //   cy.wait(500)
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-plus').click()
  //   cy.get('.v-dialog input').eq(0).type(newUnit.name)

  //   cy.intercept('POST', '/units', {
  //     body: { messages: ['Name is already existed'] },
  //     statusCode: 400
  //   })
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('i.mdi-close').first().click()
  //   cy.get('div.Vue-Toastification__toast-body').should('contain', 'Name is already existed')
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('.v-list-item > span').should('length', 3)
  // })

  // it('should success update unit', () => {
  //   cy.wait(500)
  //   cy.get('.v-list-item > span').eq(2).click()
  //   cy.intercept(
  //     {
  //       pathname: '/common/get-pronunciation',
  //       query: {
  //         text: updateUnit.name
  //       }
  //     },
  //     { statusCode: 200, body: updateUnit.name }
  //   ).as('toYomiUpdate')
  //   cy.get('.v-dialog input:first').clear().type(updateUnit.name)
  //   cy.wait('@toYomiUpdate')

  //   cy.intercept('GET', '/units', { body: [...units, updateUnit] })
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.wait('@updateUnit').its('request.body').should('deep.equal', {
  //     name: updateUnit.name,
  //     yomi: updateUnit.name
  //   })
  //   cy.get('.v-list-item > span').eq(2).should('contain', updateUnit.name)
  // })

  // it('should fail update unit name exits', () => {
  //   cy.wait(500)
  //   cy.get('.v-list-item > span').eq(2).click()
  //   cy.get('.v-dialog input:first').clear().type(updateUnit.name)

  //   cy.intercept('PUT', `/units/${newUnit.id}`, {
  //     body: { messages: ['Name is already existed'] },
  //     statusCode: 400
  //   })
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('i.mdi-close').first().click()
  //   cy.get('div.Vue-Toastification__toast-body').should('contain', 'Name is already existed')
  //   cy.get('button.Vue-Toastification__close-button').click()
  // })

  // it('should success delete unit', () => {
  //   cy.wait(500)
  //   cy.get('.v-list-item > span').eq(2).click()
  //   cy.get('span').contains('Delete').click()
  //   cy.get('span.red--text').contains('Delete').click()
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('.v-list-item > span').should('length', 2)
  // })

  // it('should fail delete unit when cancel', () => {
  //   cy.get('.v-list-item > span').eq(1).click()
  //   cy.get('.light_red').contains('Delete').click()
  //   cy.get('span.blue--text').contains('キャンセル').click()
  //   cy.get('.v-card__title').contains('Edit unit').should('length', 1)
  //   cy.get('i.v-icon.mdi-close').click()
  //   cy.get('.v-list-item > span').should('length', 2)
  // })

  // it('should fail delete unit when it is used in order', () => {
  //   cy.wait(500)
  //   cy.get('.v-list-item > span').eq(1).click()
  //   cy.get('.light_red').contains('Delete').click()

  //   cy.intercept('DELETE', `/units/${units[1].id}`, {
  //     body: {
  //       messages: [`Can not delete. This unit is used in Order detail: ID=${units[1].id}`]
  //     },
  //     statusCode: 400
  //   })
  //   cy.get('span.red--text').contains('Delete').click()
  //   cy.get('.Vue-Toastification__toast-body').contains(
  //     'Can not delete. This unit is used in Order detail: ID=2'
  //   )
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('i.v-icon.mdi-close').click()
  //   cy.get('.v-list-item > span').should('length', 2)
  // })

  // it('should sort by name and show info message, buttons', () => {
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-sort-ascending').click()
  //   cy.get('.v-bottom-sheet').should('be.visible')
  //   cy.get('span.v-btn__content').contains('Sort ascending by name').click()
  //   cy.get('span').contains('Unit list is sorted').should('be.visible')
  //   cy.get('span').contains('Click [Save] button on the top right to save').should('be.visible')
  //   cy.get('.v-list-item > span').should(($span) => {
  //     expect($span.eq(0)).to.contain('1second unit name')
  //     expect($span.eq(1)).to.contain('first unit name')
  //   })
  //   cy.get('i.mdi-close').should('be.visible')
  //   cy.get('i.mdi-content-save').should('be.visible')
  // })

  // it('should cancel sort by name and hide info message, buttons', () => {
  //   cy.wait(150)
  //   cy.get('i.mdi-close').first().click()
  //   cy.get('.v-list-item > span').should(($span) => {
  //     expect($span.eq(0)).to.contain('first unit name')
  //     expect($span.eq(1)).to.contain('1second unit name')
  //   })
  //   cy.get('i.mdi-close').should('not.be.visible')
  //   cy.get('i.mdi-content-save').should('not.exist')
  //   cy.get('span').contains('Unit list is sorted').should('not.exist')
  //   cy.get('span').contains('Click [Save] button on the top right to save').should('not.exist')
  // })

  // it('should save sort by name order and hide info message, buttons', () => {
  //   cy.wait(150)
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-sort-ascending').click()
  //   cy.get('span.v-btn__content').contains('Sort ascending by name').click()
  //   cy.get('i.mdi-content-save').click()
  //   cy.wait('@sortUnit').its('request.body').should('deep.equal', order)
  //   cy.get('.Vue-Toastification__toast-body').should('contain', 'Save order successful')
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('i.mdi-close').should('not.be.visible')
  //   cy.get('i.mdi-content-save').should('not.exist')
  //   cy.get('span').contains('Unit list is sorted').should('not.exist')
  //   cy.get('span').contains('Click [Save] button on the top right to save').should('not.exist')
  // })
})
