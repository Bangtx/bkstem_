describe('Master size page', () => {
  const commonSizes = [
    {
      name: 'first size name',
      name_eng: 'test',
      yomi: 'yomi',
      id: 1,
      order_num: 1,
      item_id: null,
      vairety_id: null,
      search_str: 'first size nameサイズyomitest',
      active: true,
      created_at: '2021-05-26',
      created_by: null
    },
    {
      name: 'second size name',
      name_eng: 'name eng',
      yomi: null,
      id: 2,
      order_num: 2,
      item_id: null,
      vairety_id: null,
      search_str: 'second size name box l',
      active: true,
      created_at: '2021-05-26',
      created_by: null
    }
  ]

  const itemSizes = [
    {
      id: 1,
      name: 'item 1',
      sizes: [
        {
          name: 'first size name',
          name_eng: 'test',
          yomi: 'yomi',
          id: 1,
          order_num: 1,
          item_id: 1,
          vairety_id: null,
          search_str: 'first size nameサイズyomitest',
          active: true,
          created_at: '2021-05-26',
          created_by: null
        }
      ]
    },
    {
      id: 2,
      name: 'item 2',
      sizes: [
        {
          name: 'first size name',
          name_eng: 'test',
          yomi: 'yomi',
          id: 1,
          order_num: 1,
          item_id: 2,
          vairety_id: null,
          search_str: 'first size nameサイズyomitest',
          active: true,
          created_at: '2021-05-26',
          created_by: null
        },
        {
          name: 'second size name',
          name_eng: 'name eng',
          yomi: null,
          id: 2,
          order_num: 2,
          item_id: 2,
          vairety_id: null,
          search_str: 'second size name box l',
          active: true,
          created_at: '2021-05-26',
          created_by: null
        }
      ]
    }
  ]

  const varietySizes = [
    {
      id: 1,
      name: 'variety 1',
      sizes: [
        {
          name: 'first size name',
          name_eng: 'test',
          yomi: 'yomi',
          id: 1,
          order_num: 1,
          item_id: null,
          vairety_id: 1,
          search_str: 'first size nameサイズyomitest',
          active: true,
          created_at: '2021-05-26',
          created_by: null
        }
      ]
    },
    {
      id: 2,
      name: 'variety 2',
      sizes: [
        {
          name: 'first size name',
          name_eng: 'test',
          yomi: 'yomi',
          id: 1,
          order_num: 1,
          item_id: null,
          vairety_id: 2,
          search_str: 'first size nameサイズyomitest',
          active: true,
          created_at: '2021-05-26',
          created_by: null
        },
        {
          name: 'second size name',
          name_eng: 'name eng',
          yomi: null,
          id: 2,
          order_num: 2,
          item_id: null,
          vairety_id: 2,
          search_str: 'second size name box l',
          active: true,
          created_at: '2021-05-26',
          created_by: null
        }
      ]
    }
  ]

  const newSize = {
    name: 'third size name',
    name_eng: 'name eng',
    yomi: 'yomi',
    id: 3,
    order_num: 3,
    search_str: 'third size name',
    active: true,
    created_at: '2021-05-26',
    created_by: null
  }

  // const newSizeNameEmpty = {
  //   name: '    ',
  //   name_eng: 'name eng',
  //   yomi: '',
  //   id: 4,
  //   order_num: 4,
  //   search_str: 'size with name empty',
  //   active: true,
  //   created_at: '2021-05-28',
  //   created_by: null
  // }

  // const updateSize = {
  //   name: 'third size name update',
  //   name_eng: 'name eng update',
  //   yomi: 'yomi',
  //   id: 3,
  //   order_num: 3,
  //   search_str: 'third size name',
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

  const itemList = [
    {
      id: 1,
      name: 'item 1'
    },
    {
      id: 2,
      name: 'item 2'
    }
  ]

  const varietyList = [
    {
      id: 1,
      name: 'variety 1'
    },
    {
      id: 2,
      name: 'variety 2'
    }
  ]

  beforeEach(() => {
    cy.intercept('GET', '/sizes/get_size_by_type?get_size=common', {
      statusCode: 200,
      body: commonSizes
    }).as('getCommonSizes')
    cy.intercept('GET', '/sizes/get_size_by_type?get_size=by_item', {
      statusCode: 200,
      body: itemSizes
    }).as('getItemSizes')
    cy.intercept('GET', '/sizes/get_size_by_type?get_size=by_variety', {
      statusCode: 200,
      body: varietySizes
    }).as('getVarietySizes')
    cy.intercept('GET', '/varieties/get_varieties_for_list_selecting', {
      statusCode: 200,
      body: varietyList
    }).as('getVarietyList')
    cy.intercept('GET', '/items/get_items_for_list_selecting', {
      statusCode: 200,
      body: itemList
    }).as('getItemList')

    cy.intercept('POST', '/sizes', { statusCode: 200, body: newSize }).as('createSize')

    cy.intercept('PUT', `/sizes/${newSize.id}`, { statusCode: 200, body: newSize }).as('updateSize')

    cy.intercept('DELETE', `/sizes/${newSize.id}`, { statusCode: 200, body: newSize.id })

    cy.intercept('POST', '/sizes/sort', { statusCode: 200, body: { detail: 'Sort Size' } }).as(
      'sortSize'
    )
    cy.intercept(
      {
        pathname: '/common/get-pronunciation',
        query: {
          text: newSize.name
        }
      },
      { statusCode: 200, body: newSize.name }
    )
  })

  it('should display list common size', () => {
    cy.visit('/master/sizes')
    cy.wait('@getCommonSizes')

    cy.get('.v-list-item > span').should(($span) => {
      expect($span).to.have.length(2)
      expect($span.eq(0)).to.contain('first size name')
      expect($span.eq(1)).to.contain('second size name')
    })
  })

  it('should display search common size by name', () => {
    cy.get('input').should('exist').type('first')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first size name')

    cy.get('input').should('exist').clear()
    cy.get('.v-list-item > span').should('length', 2)

    cy.get('input').should('exist').type('second')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'second size name')
  })

  it('should search common size by yomi', () => {
    cy.get('input').should('exist').clear().type('yomi')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first size name')
  })

  it('should search common size by name eng', () => {
    cy.get('input').should('exist').clear().type('test')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first size name')
  })

  it('should search common size with upper characters', () => {
    cy.get('input').should('exist').clear().type('BOX L')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'second size name')
  })

  it('should search common size by half width', () => {
    cy.get('input').should('exist').clear().type('ｻｲｽﾞ')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first size name')
  })

  it('should search common size render empty', () => {
    cy.get('input').should('exist').type('abcxyz')
    cy.get('.v-list-item > span').should('length', 0)
    cy.get('input').should('exist').clear()
  })

  it('should display commons size information', () => {
    cy.get('.v-list-item > span').first().click()
    cy.get('.v-dialog input:first').should('have.value', 'first size name')
    cy.get('.v-dialog input').eq(1).should('have.value', 'yomi')
    cy.get('.v-dialog input').eq(2).should('have.value', 'test')
    cy.get('i.mdi-close').click()
  })

  // to this

  // it('should success create new size', () => {
  //   cy.wait(200)
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-plus').click()
  //   cy.get('.v-dialog input').eq(0).type(newSize.name)
  //   cy.get('.v-dialog input').eq(1).should('have.value', newSize.name)
  //   cy.get('.v-dialog input').eq(1).clear().type(newSize.yomi)
  //   cy.get('.v-dialog input').eq(2).type(newSize.name_eng)

  //   cy.intercept('GET', '/sizes', { statusCode: 200, body: [...sizes, newSize] })
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.wait('@createSize')
  //     .its('request.body')
  //     .should('deep.equal', { name: newSize.name, name_eng: newSize.name_eng, yomi: newSize.yomi })
  //   cy.get('i.mdi-close').first().click()
  //   cy.get('.v-list-item > span').should('length', 3)
  //   cy.get('.v-list-item > span').eq(2).should('contain', 'third size name')
  // })

  // it('should fail create new size when name empty', () => {
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-plus').click()
  //   cy.get('.v-dialog input').eq(0).type(newSizeNameEmpty.name)
  //   cy.get('.v-dialog input').eq(2).type(newSizeNameEmpty.name_eng)
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('.v-dialog input').eq(0).should('be.empty')
  //   cy.get('.v-dialog input').eq(1).should('be.empty')
  //   cy.get('.Vue-Toastification__toast-body').should('contain', 'Cannot save, name is empty')
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('i.mdi-close').click()
  //   cy.get('.v-list-item > span').should('length', 3)
  // })

  // it('should fail create new size when name exits', () => {
  //   cy.wait(500)
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-plus').click()
  //   cy.get('.v-dialog input').eq(0).type(newSize.name)
  //   cy.get('.v-dialog input').eq(1).clear().type(newSize.yomi)
  //   cy.get('.v-dialog input').eq(2).clear().type(newSize.name_eng)

  //   cy.intercept('POST', '/sizes', {
  //     statusCode: 400,
  //     body: { messages: ['Name is already existed'] }
  //   })
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('div.Vue-Toastification__toast-body').should('contain', 'Name is already existed')
  //   cy.get('i.mdi-close').first().click()
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('.v-list-item > span').should('length', 3)
  // })

  // it('should success update size', () => {
  //   cy.get('.v-list-item > span').eq(2).click()
  //   cy.get('.v-dialog input:first').clear().type(updateSize.name)
  //   cy.get('.v-dialog input').eq(1).clear().type(updateSize.yomi)
  //   cy.get('.v-dialog input').eq(2).clear().type(updateSize.name_eng)

  //   cy.intercept('GET', '/sizes', { body: [...sizes, updateSize] })
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.wait('@updateSize').its('request.body').should('deep.equal', {
  //     name: updateSize.name,
  //     name_eng: updateSize.name_eng,
  //     yomi: updateSize.yomi
  //   })
  //   cy.get('.v-list-item > span').eq(2).should('contain', updateSize.name)
  // })

  // it('should fail update size name exits', () => {
  //   cy.get('.v-list-item > span').eq(2).click()
  //   cy.get('.v-dialog input:first').clear().type(updateSize.name)
  //   cy.get('.v-dialog input').eq(1).clear().type(updateSize.yomi)
  //   cy.get('.v-dialog input').eq(2).clear().type(updateSize.name_eng)

  //   cy.intercept('PUT', `/sizes/${newSize.id}`, {
  //     statusCode: 400,
  //     body: { messages: ['Name is already existed'] }
  //   })
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('i.mdi-close').first().click()
  //   cy.get('div.Vue-Toastification__toast-body').should('contain', 'Name is already existed')
  //   cy.get('button.Vue-Toastification__close-button').click()
  // })

  // it('should success delete size', () => {
  //   cy.wait(500)
  //   cy.get('.v-list-item > span').eq(2).click()
  //   cy.get('span').contains('Delete').click()
  //   cy.get('span.red--text').contains('Delete').click()
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('.v-list-item > span').should('length', 2)
  // })

  // it('should fail delete size when cancel', () => {
  //   cy.get('.v-list-item > span').eq(1).click()
  //   cy.get('.light_red').contains('Delete').click()
  //   cy.get('span.blue--text').contains('キャンセル').click()
  //   cy.get('.v-card__title').contains('Edit size').should('length', 1)
  //   cy.get('i.v-icon.mdi-close').click()
  //   cy.get('.v-list-item > span').should('length', 2)
  // })

  // it('should fail delete size when it is used in order', () => {
  //   cy.wait(500)
  //   cy.get('.v-list-item > span').eq(1).click()
  //   cy.get('.light_red').contains('Delete').click()

  //   cy.intercept('DELETE', `/sizes/${sizes[1].id}`, {
  //     statusCode: 400,
  //     body: {
  //       messages: [`Can not delete. This size is used in Order detail: ID=${sizes[1].id}`]
  //     }
  //   })
  //   cy.get('span.red--text').contains('Delete').click()
  //   cy.get('.Vue-Toastification__toast-body').contains(
  //     'Can not delete. This size is used in Order detail: ID=2'
  //   )
  //   cy.get('button.Vue-Toastification__close-button').click({ multiple: true })
  //   cy.get('i.v-icon.mdi-close').click()
  //   cy.get('.v-list-item > span').should('length', 2)
  // })

  // it('should sort by name and show info message, buttons', () => {
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-sort-ascending').click()
  //   cy.get('.v-bottom-sheet').should('be.visible')
  //   cy.get('span.v-btn__content').contains('Sort ascending by name').click()
  //   cy.get('span').contains('Size list is sorted').should('be.visible')
  //   cy.get('span').contains('Click [Save] button on the top right to save').should('be.visible')
  //   cy.get('.v-list-item > span').should(($span) => {
  //     expect($span.eq(0)).to.contain('first size name')
  //     expect($span.eq(1)).to.contain('second size name')
  //   })
  //   cy.get('i.mdi-close').should('be.visible')
  //   cy.get('i.mdi-content-save').should('be.visible')
  // })

  // it('should cancel sort by name and hide info message, buttons', () => {
  //   cy.wait(150)
  //   cy.get('i.mdi-close').first().click()
  //   cy.get('i.mdi-close').should('not.be.visible')
  //   cy.get('i.mdi-content-save').should('not.exist')
  //   cy.get('span').contains('Size list is sorted').should('not.exist')
  //   cy.get('span').contains('Click [Save] button on the top right to save').should('not.exist')
  // })

  // it('should save sort by name order and hide info message, buttons', () => {
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-sort-ascending').click()
  //   cy.get('span.v-btn__content').contains('Sort ascending by name').click()
  //   cy.get('i.mdi-content-save').click()
  //   cy.wait('@sortSize').its('request.body').should('deep.equal', order)
  //   cy.get('.Vue-Toastification__toast-body').should('contain', 'Save order successful')
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('i.mdi-close').should('not.be.visible')
  //   cy.get('i.mdi-content-save').should('not.exist')
  //   cy.get('span').contains('Size list is sorted').should('not.exist')
  //   cy.get('span').contains('Click [Save] button on the top right to save').should('not.exist')
  //   cy.get('.v-list-item > span').should(($span) => {
  //     expect($span.eq(0)).to.contain('first size name')
  //     expect($span.eq(1)).to.contain('second size name')
  //   })
  // })

  // item size
  it('should display list first item size', () => {
    cy.visit('/master/sizes')
    cy.get('.v-tabs-bar__content > div').eq(1).click()
    cy.wait('@getItemSizes')
    cy.get('.v-list-item > span').should(($span) => {
      expect($span).to.have.length(1)
      expect($span.eq(0)).to.contain('first size name')
    })
  })

  it('should display list second item size', () => {
    cy.get('.v-input').eq(0).click()
    cy.get('.v-select-list > .v-list-item').should(($span) => {
      expect($span).to.have.length(2)
      expect($span.eq(0)).to.contain('item 1')
      expect($span.eq(1)).to.contain('item 2')
    })
    cy.get('.v-select-list > .v-list-item').eq(1).click()
    cy.get('.v-list-item > span').should(($span) => {
      expect($span).to.have.length(2)
      expect($span.eq(0)).to.contain('first size name')
      expect($span.eq(1)).to.contain('second size name')
    })
  })

  it('should display search item by name', () => {
    cy.get('input').eq(0).should('exist').clear()
    cy.get('input').eq(0).should('exist').type('item 1')
    cy.get('.v-select-list > .v-list-item').should(($span) => {
      expect($span).to.have.length(1)
    })
    cy.get('input').eq(0).should('exist').clear()
  })

  it('should display search item size by name', () => {
    cy.get('input').eq(2).should('exist').type('first')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first size name')

    cy.get('input').eq(2).should('exist').clear()
    cy.get('.v-list-item > span').should('length', 2)

    cy.get('input').eq(2).should('exist').type('second')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'second size name')
  })

  it('should search item size by yomi', () => {
    cy.get('input').eq(2).should('exist').clear().type('yomi')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first size name')
  })

  it('should search item size by name eng', () => {
    cy.get('input').eq(2).should('exist').clear().type('test')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first size name')
  })

  it('should search item size with upper characters', () => {
    cy.get('input').eq(2).should('exist').clear().type('BOX L')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'second size name')
  })

  it('should search item size by half width', () => {
    cy.get('input').eq(2).should('exist').clear().type('ｻｲｽﾞ')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first size name')
  })

  it('should search item size render empty', () => {
    cy.get('input').eq(2).should('exist').type('abcxyz')
    cy.get('.v-list-item > span').should('length', 0)
    cy.get('input').eq(2).should('exist').clear()
  })

  it('should display item size information', () => {
    cy.get('.v-list-item > span').first().click()
    cy.wait('@getItemList')
    cy.get('.v-select__selections').should('contain', 'item 2')
    cy.get('.v-dialog input').eq(2).should('have.value', 'first size name')
    cy.get('.v-dialog input').eq(3).should('have.value', 'yomi')
    cy.get('.v-dialog input').eq(4).should('have.value', 'test')
    cy.get('i.mdi-close').click()
  })

  // variety size
  it('should display list first variety size', () => {
    cy.visit('/master/sizes')
    cy.get('.v-tabs-bar__content > div').eq(2).click()
    cy.wait('@getVarietySizes')
    cy.get('.v-list-item > span').should(($span) => {
      expect($span).to.have.length(1)
      expect($span.eq(0)).to.contain('first size name')
    })
  })

  it('should display list second variety size', () => {
    cy.get('.v-input').eq(0).click()
    cy.get('.v-select-list > .v-list-item').should(($span) => {
      expect($span).to.have.length(2)
      expect($span.eq(0)).to.contain('variety 1')
      expect($span.eq(1)).to.contain('variety 2')
    })
    cy.get('.v-select-list > .v-list-item').eq(1).click()
    cy.get('.v-list-item > span').should(($span) => {
      expect($span).to.have.length(2)
      expect($span.eq(0)).to.contain('first size name')
      expect($span.eq(1)).to.contain('second size name')
    })
  })

  it('should display search variety by name', () => {
    cy.get('input').eq(0).should('exist').clear()
    cy.get('input').eq(0).should('exist').type('variety 1')
    cy.get('.v-select-list > .v-list-item').should(($span) => {
      expect($span).to.have.length(1)
    })
    cy.get('input').eq(0).should('exist').clear()
  })

  it('should display search variety size by name', () => {
    cy.get('input').eq(2).should('exist').type('first')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first size name')

    cy.get('input').eq(2).should('exist').clear()
    cy.get('.v-list-item > span').should('length', 2)

    cy.get('input').eq(2).should('exist').type('second')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'second size name')
  })

  it('should search variety size by yomi', () => {
    cy.get('input').eq(2).should('exist').clear().type('yomi')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first size name')
  })

  it('should search variety size by name eng', () => {
    cy.get('input').eq(2).should('exist').clear().type('test')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first size name')
  })

  it('should search variety size with upper characters', () => {
    cy.get('input').eq(2).should('exist').clear().type('BOX L')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'second size name')
  })

  it('should search variety size by half width', () => {
    cy.get('input').eq(2).should('exist').clear().type('ｻｲｽﾞ')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first size name')
  })

  it('should search variety size render empty', () => {
    cy.get('input').eq(2).should('exist').type('abcxyz')
    cy.get('.v-list-item > span').should('length', 0)
    cy.get('input').eq(2).should('exist').clear()
  })

  it('should display variety size information', () => {
    cy.get('.v-list-item > span').first().click()
    cy.wait('@getVarietyList')
    cy.get('.v-select__selections').should('contain', 'variety 2')
    cy.get('.v-dialog input').eq(2).should('have.value', 'first size name')
    cy.get('.v-dialog input').eq(3).should('have.value', 'yomi')
    cy.get('.v-dialog input').eq(4).should('have.value', 'test')
    cy.get('i.mdi-close').click()
  })
})
