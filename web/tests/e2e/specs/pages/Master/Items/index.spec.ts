describe('Master item page', () => {
  const items = [
    {
      name: '2first item nameアーティチョーク',
      name_eng: 'first name eng',
      short_name: 'first short name',
      yomi: 'first yomi',
      id: 1,
      order_num: 1,
      search_str: '2first item nameアーティチョークfirst name engfirst short namefirst yomi',
      active: true,
      created_at: '2021-06-15',
      created_by: null,
      images: [],
      default_unit: {
        id: 1,
        name: 'Unit 1'
      },
      units: [
        {
          id: 1,
          name: 'Unit 1'
        }
      ]
    },
    {
      name: '1second item name',
      name_eng: 'second name eng',
      short_name: 'second short name',
      yomi: '1second item name',
      id: 2,
      order_num: 2,
      search_str: '1second item namesecond name engsecond short name',
      active: true,
      created_at: '2021-06-15',
      created_by: null,
      images: [],
      default_unit: {
        id: 2,
        name: 'Unit 2'
      },
      units: [
        {
          id: 2,
          name: 'Unit 2'
        }
      ]
    }
  ]

  const newItem = {
    name: 'third item name',
    name_eng: 'name eng',
    short_name: 'short name',
    yomi: 'third item name',
    id: 3,
    order_num: 3,
    search_str: 'third item namename engshort name',
    active: true,
    created_at: '2021-06-15',
    created_by: null,
    images: [],
    default_unit: {
      id: 1,
      name: 'Unit 1'
    },
    units: [
      {
        id: 1,
        name: 'Unit 1'
      }
    ]
  }

  // const newItemNameEmpty = {
  //   name: '    ',
  //   name_eng: 'name eng',
  //   short_name: 'short name',
  //   yomi: '',
  //   id: 4,
  //   order_num: 4,
  //   search_str: 'item with name empty',
  //   active: true,
  //   created_at: '2021-06-15',
  //   created_by: null,
  //   images: [],
  //   default_unit: {
  //     id: 1,
  //     name: 'Unit 1'
  //   }
  // }

  const updateItem = {
    name: 'third item name',
    name_eng: 'name eng update',
    short_name: 'third short name',
    yomi: 'third item name',
    id: 3,
    order_num: 3,
    search_str: 'third item namename eng updatethird short nam',
    active: true,
    created_at: '2021-06-15',
    created_by: null,
    images: [],
    default_unit: {
      id: 1,
      name: 'Unit 1'
    },
    units: [
      {
        id: 1,
        name: 'Unit 1'
      }
    ]
  }

  const units = [
    {
      id: 1,
      name: 'Unit 1',
      order_num: 1,
      search_str: '',
      active: true,
      created_at: '2021-06-11',
      created_by: null
    },
    {
      id: 2,
      name: 'Unit 2',
      order_num: 2,
      search_str: '',
      active: true,
      created_at: '2021-06-11',
      created_by: null
    }
  ]

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
    cy.intercept('GET', '/items', { statusCode: 200, body: items }).as('getItems')
    cy.intercept('GET', '/units', { statusCode: 200, body: units }).as('getUnits')

    cy.intercept('POST', '/items', {
      statusCode: 200,
      body: newItem
    }).as('createItem')

    cy.intercept('PUT', `/items/${updateItem.id}`, { statusCode: 200, body: updateItem }).as(
      'updateItem'
    )

    cy.intercept('DELETE', `/items/${newItem.id}`, { statusCode: 200, body: newItem.id })

    cy.intercept('POST', '/items/sort', { statusCode: 200, body: { detail: 'Sort Item' } }).as(
      'sortItem'
    )

    cy.intercept(
      {
        pathname: '/common/get-pronunciation',
        query: {
          text: newItem.name
        }
      },
      { statusCode: 200, body: newItem.name }
    ).as('toYomi')
  })

  it('should display list item', () => {
    cy.visit('/master/items')
    cy.wait('@getItems')
    cy.get('.v-list-item > span').should(($span) => {
      expect($span).to.have.length(2)
      expect($span.eq(0)).to.contain('2first item nameアーティチョーク')
      expect($span.eq(1)).to.contain('1second item name')
    })
  })

  it('should search item by name', () => {
    cy.get('input').should('exist').type('first')
    cy.get('.v-list-item > span')
      .should('length', 1)
      .should('contain', '2first item nameアーティチョーク')

    cy.get('input').should('exist').clear()
    cy.get('.v-list-item > span').should(($span) => {
      expect($span).to.have.length(2)
      expect($span.eq(0)).to.contain('2first item nameアーティチョーク')
      expect($span.eq(1)).to.contain('1second item name')
    })

    cy.get('input').should('exist').type('second')
    cy.get('.v-list-item > span').should('length', 1).should('contain', '1second item name')
    cy.get('input').should('exist').clear()
  })

  it('should search item by short name', () => {
    cy.get('input').should('exist').type('first short name')
    cy.get('.v-list-item > span').should('contain', '2first item nameアーティチョーク')
    cy.get('input').should('exist').clear()
  })

  it('should search item by yomi', () => {
    cy.get('input').should('exist').type('yomi')
    cy.get('.v-list-item > span').should('contain', '2first item nameアーティチョーク')
    cy.get('input').should('exist').clear()
  })

  it('should search item by name eng', () => {
    cy.get('input').should('exist').type('first name eng')
    cy.get('.v-list-item > span').should('contain', '2first item nameアーティチョーク')
    cy.get('input').should('exist').clear()
  })

  it('should search item by name (half width)', () => {
    cy.get('input').should('exist').type('ｱｰﾃｨﾁｮｰｸ')
    cy.get('.v-list-item > span')
      .should('length', 1)
      .should('contain', '2first item nameアーティチョーク')
    cy.get('input').should('exist').clear()
  })

  it('should search item by name (upper characters)', () => {
    cy.get('input').should('exist').type('FIRST')
    cy.get('.v-list-item > span')
      .should('length', 1)
      .should('contain', '2first item nameアーティチョーク')
    cy.get('input').should('exist').clear()
  })

  it('should search item render empty', () => {
    cy.get('input').should('exist').type('acsdvdf')
    cy.get('.row').should('contain', 'There is no item')
    cy.get('input').should('exist').clear()
  })

  it('should display item information', () => {
    cy.get('.v-list-item > span').first().click()
    cy.get('.v-dialog input').eq(1).should('have.value', '2first item nameアーティチョーク')
    cy.get('.v-dialog input').eq(2).should('have.value', 'first short name')
    cy.get('.v-dialog input').eq(3).should('have.value', 'first yomi')
    cy.get('.v-dialog input').eq(4).should('have.value', 'first name eng')
    cy.get('.defaultunit').should('contain', 'Default unit: Unit 1')
    cy.get('i.mdi-close').click()
  })

  // it('should success create new item', () => {
  //   cy.wait(200)
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-plus').click()
  //   cy.get('.v-dialog input').eq(1).type(newItem.name)
  //   cy.get('.v-dialog input').eq(2).type(newItem.short_name)
  //   cy.get('.v-dialog input').eq(4).type(newItem.name_eng)

  //   cy.intercept('GET', '/items', { body: [...items, newItem] })
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.wait('@createItem').its('request.body').should('deep.equal', {
  //     name: newItem.name,
  //     name_eng: newItem.name_eng,
  //     short_name: newItem.short_name,
  //     yomi: newItem.name,
  //     default_unit: newItem.default_unit.id
  //   })
  //   cy.get('i.mdi-close').click()
  //   cy.get('.v-list-item > span').should('length', 3)
  //   cy.get('.v-list-item > span').eq(2).should('contain', 'third item name')
  // })

  // it('should fail when create new item with name empty', () => {
  //   cy.wait(200)
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-plus').click()
  //   cy.get('.v-dialog input').eq(1).type(newItemNameEmpty.name)
  //   cy.get('.v-dialog input').eq(2).type(newItemNameEmpty.short_name)
  //   cy.get('.v-dialog input').eq(3).type(newItemNameEmpty.name_eng)
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('.Vue-Toastification__toast-body').should('contain', 'Can not save, name is empty')
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('i.mdi-close').click()
  //   cy.get('.v-list-item > span').should('length', 3)
  // })

  // it('should fail create new item when name exits', () => {
  //   cy.wait(200)
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-plus').click()
  //   cy.get('.v-dialog input').eq(1).type(newItem.name)
  //   cy.get('.v-dialog input').eq(2).type(newItem.short_name)
  //   cy.get('.v-dialog input').eq(3).type(newItem.name_eng)
  //   cy.intercept('POST', '/items', {
  //     body: { messages: ['Name is already existed'] },
  //     statusCode: 400
  //   }).as('postNameExits')
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.wait('@postNameExits')
  //   cy.get('div.Vue-Toastification__toast-body').should('contain', 'Name is already existed')
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('i.mdi-close').click()
  //   cy.get('.v-list-item > span').should('length', 3)
  //   cy.get('.v-list-item > span').eq(2).should('contain', 'third item name')
  // })

  // it('should fill yomi automatically', () => {
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-plus').click()
  //   cy.get('.v-dialog input').eq(1).clear().type(updateItem.name)
  //   cy.wait('@toYomi')
  //   cy.wait(500)
  //   cy.get('.v-dialog input').eq(3).should('have.value', newItem.name)
  //   cy.get('i.mdi-close').click()
  // })

  // it('should success update item', () => {
  //   cy.get('.v-list-item > span').eq(2).click()
  //   cy.get('.v-dialog input').eq(1).clear().type(updateItem.name)
  //   cy.get('.v-dialog input').eq(2).clear().type(updateItem.short_name)
  //   cy.get('.v-dialog input').eq(4).clear().type(updateItem.name_eng)

  //   cy.intercept('GET', '/items', { body: [...items, updateItem] })
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.wait('@updateItem').its('request.body').should('deep.equal', {
  //     name: updateItem.name,
  //     name_eng: updateItem.name_eng,
  //     short_name: updateItem.short_name,
  //     yomi: newItem.yomi,
  //     default_unit: updateItem.default_unit.id
  //   })
  //   cy.get('.v-list-item > span').eq(2).should('contain', updateItem.name)
  //   cy.get('.Vue-Toastification__toast--success').should('contain', 'Update successfully')
  //   cy.get('button.Vue-Toastification__close-button').click()
  // })

  // it('should fail update item name exits', () => {
  //   cy.get('.v-list-item > span').eq(2).click()
  //   cy.get('.v-dialog input').eq(1).clear().type(updateItem.name)

  //   cy.intercept('PUT', `/items/${updateItem.id}`, {
  //     body: { messages: ['Name is already existed'] },
  //     statusCode: 400
  //   })
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('.v-list-item > span').eq(2).should('contain', updateItem.name)
  //   cy.get('.Vue-Toastification__toast--error').should('contain', 'Name is already existed')
  //   cy.get('button.Vue-Toastification__close-button').click({ multiple: true })
  //   cy.get('i.mdi-close').click()
  // })

  // it('should success delete item', () => {
  //   cy.get('.v-list-item > span').eq(2).click()
  //   cy.get('span').contains('Delete').click()
  //   cy.get('span.red--text').contains('Delete').click()
  //   cy.get('.v-list-item > span').should('length', 2)
  //   cy.get('button.Vue-Toastification__close-button').click()
  // })

  // it('should fail delete item when cancel', () => {
  //   cy.get('.v-list-item > span').eq(1).click()
  //   cy.get('.light_red').contains('Delete').click()
  //   cy.get('span.blue--text').contains('キャンセル').click()
  //   cy.get('i.v-icon.mdi-close').click()
  //   cy.get('.v-list-item > span').should('length', 2)
  // })

  // it('should fail delete item when it is used in order', () => {
  //   cy.wait(500)
  //   cy.get('.v-list-item > span').eq(1).click()
  //   cy.get('.light_red').contains('Delete').click()

  //   cy.intercept('DELETE', `/items/${items[1].id}`, {
  //     body: {
  //       messages: [`Can not delete. This size is used in Order detail: ID=${items[1].id}`]
  //     },
  //     statusCode: 400
  //   })
  //   cy.get('span.red--text').contains('Delete').click()
  //   cy.get('.Vue-Toastification__toast-body').contains(
  //     'Can not delete. This size is used in Order detail: ID=2'
  //   )
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('.v-list-item > span').should('length', 2)
  // })

  // it('should sort by name and show info message, buttons', () => {
  //   cy.wait(1000)
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-sort-ascending').click()
  //   cy.get('.v-bottom-sheet').should('be.visible')
  //   cy.get('span.v-btn__content').contains('Sort ascending by name').click()
  //   cy.get('span').contains('Item list is sorted').should('be.visible')
  //   cy.get('span').contains('Click [Save] button on the top right to save').should('be.visible')
  //   cy.get('.v-list-item > span').should(($span) => {
  //     expect($span.eq(0)).to.contain('1second item name')
  //     expect($span.eq(1)).to.contain('2first item nameアーティチョーク')
  //   })
  //   cy.get('i.mdi-close').should('be.visible')
  //   cy.get('i.mdi-content-save').should('be.visible')
  // })

  // it('should cancel sort by name and hide info message, buttons', () => {
  //   cy.wait(150)
  //   cy.get('i.mdi-close').first().click()
  //   cy.get('.v-list-item > span').should(($span) => {
  //     expect($span.eq(0)).to.contain('2first item nameアーティチョーク')
  //     expect($span.eq(1)).to.contain('1second item name')
  //   })
  //   cy.get('i.mdi-close').should('not.be.visible')
  //   cy.get('i.mdi-content-save').should('not.exist')
  //   cy.get('span').contains('Item list is sorted').should('not.exist')
  //   cy.get('span').contains('Click [Save] button on the top right to save').should('not.exist')
  // })

  // it('should save sort by name order and hide info message, buttons', () => {
  //   cy.wait(150)
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-sort-ascending').click()
  //   cy.get('span.v-btn__content').contains('Sort ascending by name').click()
  //   cy.get('i.mdi-content-save').click()
  //   cy.wait('@sortItem').its('request.body').should('deep.equal', order)
  //   cy.get('.Vue-Toastification__toast-body').should('contain', 'Save order successful')
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('i.mdi-close').should('not.be.visible')
  //   cy.get('i.mdi-content-save').should('not.exist')
  //   cy.get('span').contains('Item list is sorted').should('not.exist')
  //   cy.get('span').contains('Click [Save] button on the top right to save').should('not.exist')
  // })
})
