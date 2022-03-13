describe('Master variety page', () => {
  const varietiesByItem = [
    {
      id: 1,
      name: 'Item 1',
      varieties: [
        {
          name: 'first variety nameサイズ',
          name_eng: 'first name eng',
          short_name: 'first short name',
          yomi: 'first variety yomiサイズ',
          id: 1,
          order_num: 1,
          search_str:
            'Item 1first variety nameサイズfirst name engfirst short namefirst variety yomiサイズ',
          active: true,
          created_at: '2021-06-11',
          created_by: null,
          images: [],
          item: {
            id: 1,
            name: 'Item 1'
          }
        },
        {
          name: 'second variety name',
          name_eng: 'second name eng',
          short_name: 'second short name',
          yomi: 'second variety name',
          id: 2,
          order_num: 2,
          search_str: 'Item 1second variety namesecond name engsecond short name',
          active: true,
          created_at: '2021-06-11',
          created_by: null,
          images: [],
          item: {
            id: 1,
            name: 'Item 1'
          }
        }
      ]
    },
    {
      id: 2,
      name: 'Item 2',
      varieties: [
        {
          name: 'third variety name',
          name_eng: 'third name eng',
          short_name: 'third short name',
          yomi: 'third variety name',
          id: 3,
          order_num: 1,
          search_str: 'third variety namethird name engthird short name',
          active: true,
          created_at: '2021-06-11',
          created_by: null,
          images: [],
          item: {
            id: 2,
            name: 'Item 2'
          }
        },
        {
          name: 'fourth variety name',
          name_eng: 'fourth name eng',
          short_name: 'fourth short name',
          yomi: 'fourth variety name',
          id: 4,
          order_num: 2,
          search_str: 'fourth variety namefourth name engfourth short name',
          active: true,
          created_at: '2021-06-11',
          created_by: null,
          images: [],
          item: {
            id: 2,
            name: 'Item 2'
          }
        }
      ]
    }
  ]

  const newVariety = {
    name: 'fifth variety name',
    name_eng: 'name eng',
    short_name: 'short name',
    yomi: 'fifth variety name',
    id: 5,
    order_num: 5,
    search_str: 'fifth size name',
    active: true,
    created_at: '2021-06-11',
    created_by: null,
    images: [],
    item: {
      id: 1,
      name: 'Item 1'
    }
  }

  // const newVarietyNameEmpty = {
  //   name: '    ',
  //   name_eng: 'name eng',
  //   short_name: '',
  //   yomi: '',
  //   id: 4,
  //   order_num: 4,
  //   search_str: 'size with name empty',
  //   active: true,
  //   created_at: '2021-06-11',
  //   created_by: null,
  //   images: [],
  //   item: {
  //     id: 1,
  //     name: 'Item 1'
  //   }
  // }

  const updateVariety = {
    name: 'third variety name',
    name_eng: 'name eng update',
    short_name: 'third short name',
    yomi: 'third variety name',
    id: 3,
    order_num: 3,
    search_str: 'third variety name',
    active: true,
    created_at: '2021-06-11',
    created_by: null,
    images: [],
    item: {
      id: 2,
      name: 'Item 2'
    }
  }

  const items = [
    {
      name: 'Item 1',
      name_eng: '',
      short_name: '',
      yomi: '',
      id: 1,
      order_num: 1,
      search_str: '',
      active: true,
      created_at: '2021-06-11',
      created_by: null,
      images: [],
      unit: {
        id: 1,
        name: 'Unit 1',
        order_num: 1,
        search_str: '',
        active: true,
        created_at: '2021-06-11',
        created_by: null
      }
    },
    {
      name: 'Item 2',
      name_eng: '',
      short_name: '',
      yomi: '',
      id: 2,
      order_num: 2,
      search_str: '',
      active: true,
      created_at: '2021-06-11',
      created_by: null,
      images: [],
      unit: {
        id: 1,
        name: 'Unit 1',
        order_num: 1,
        search_str: '',
        active: true,
        created_at: '2021-06-11',
        created_by: null
      }
    }
  ]

  // const orderOne = [
  //   {
  //     id: 5,
  //     order_num: 1
  //   },
  //   {
  //     id: 1,
  //     order_num: 2
  //   },
  //   {
  //     id: 2,
  //     order_num: 3
  //   }
  // ]

  // const orderAll = [
  //   {
  //     id: 5,
  //     order_num: 1
  //   },
  //   {
  //     id: 1,
  //     order_num: 2
  //   },
  //   {
  //     id: 2,
  //     order_num: 3
  //   },
  //   {
  //     id: 4,
  //     order_num: 4
  //   },
  //   {
  //     id: 3,
  //     order_num: 5
  //   }
  // ]

  beforeEach(() => {
    cy.intercept('GET', '/varieties/group_by_item', { body: varietiesByItem }).as(
      'getVarietiesByItem'
    )
    cy.intercept('GET', '/items', { body: items }).as('getItems')

    cy.intercept('POST', '/varieties', { body: newVariety, statusCode: 200 }).as('createVariety')

    cy.intercept('PUT', `/varieties/${updateVariety.id}`, {
      body: updateVariety,
      statusCode: 200
    }).as('updateVariety')

    cy.intercept('DELETE', `/varieties/${newVariety.id}`, {
      body: newVariety.id,
      statusCode: 200
    }).as('deleteVariety')

    cy.intercept('POST', '/varieties/sort', {
      statusCode: 200,
      body: { detail: 'Sort Variety' }
    }).as('sortVariety')

    cy.intercept(
      {
        pathname: '/common/get-pronunciation',
        query: {
          text: newVariety.name
        }
      },
      { statusCode: 200, body: newVariety.name }
    ).as('toYomi')
  })

  it('should display list item', () => {
    cy.visit('/master/varieties')
    cy.wait('@getVarietiesByItem')

    cy.get(
      '.scroller > .vue-recycle-scroller__item-wrapper > .vue-recycle-scroller__item-view > div'
    ).should(($div) => {
      expect($div).to.have.length(2)
      expect($div.eq(0)).to.contain('Item 1')
      expect($div.eq(1)).to.contain('Item 2')
    })
  })

  // it('should display list variety', () => {
  //   cy.get('.v-list-item__title > .v-list-item__content').first().click()
  //   cy.get('.variety').should(($span) => {
  //     expect($span).to.have.length(2)
  //     expect($span.eq(0)).to.contain('first variety nameサイズ')
  //     expect($span.eq(1)).to.contain('second variety name')
  //   })
  // })

  // it('should search variety by name', () => {
  //   cy.get('input').should('exist').type('first')
  //   cy.get('.variety').should('length', 1).should('contain', 'first variety nameサイズ')
  //   cy.get('.v-list-item__title > .v-list-item__content')
  //     .should('length', 1)
  //     .should('contain', 'Item 1')

  //   cy.get('input').should('exist').clear()
  //   cy.get('.v-list-item__title > .v-list-item__content').should('length', 2)
  //   cy.get('.variety').should(($span) => {
  //     expect($span).to.have.length(2)
  //     expect($span.eq(0)).to.contain('first variety nameサイズ')
  //     expect($span.eq(1)).to.contain('second variety name')
  //   })

  //   cy.get('input').should('exist').type('second')
  //   cy.get('.variety').should('length', 1).should('contain', 'second variety name')
  //   cy.get('input').should('exist').clear()
  // })

  // it('should search variety by item', () => {
  //   cy.get('input').should('exist').type('Item 1')
  //   cy.get('.variety').should(($span) => {
  //     expect($span).to.have.length(2)
  //     expect($span.eq(0)).to.contain('first variety nameサイズ')
  //     expect($span.eq(1)).to.contain('second variety name')
  //   })
  //   cy.get('input').should('exist').clear()
  // })

  // it('should search variety by short name', () => {
  //   cy.get('input').should('exist').type('first short name')
  //   cy.get('.variety').should('length', 1).should('contain', 'first variety nameサイズ')
  //   cy.get('input').should('exist').clear()
  // })

  // it('should search variety by yomi', () => {
  //   cy.get('input').should('exist').type('yomi')
  //   cy.get('.variety').should('length', 1).should('contain', 'first variety nameサイズ')
  //   cy.get('input').should('exist').clear()
  // })

  // it('should search variety by name eng', () => {
  //   cy.get('input').should('exist').type('first name eng')
  //   cy.get('.variety').should('length', 1).should('contain', 'first variety nameサイズ')
  //   cy.get('input').should('exist').clear()
  // })

  // it('should search variety by half width', () => {
  //   cy.get('input').should('exist').type('ｻｲｽﾞ')
  //   cy.get('.v-list-item__title > .v-list-item__content').should('length', 1).click()
  //   cy.get('.variety').should('length', 1).should('contain', 'first variety nameサイズ')
  //   cy.get('input').should('exist').clear()
  // })

  // it('should search variety with upper characters', () => {
  //   cy.get('input').should('exist').type('FIRST')
  //   cy.get('.variety').should('length', 1).should('contain', 'first variety nameサイズ')
  //   cy.get('input').should('exist').clear()
  // })

  // it('should search variety render empty', () => {
  //   cy.get('input').should('exist').type('acsdvdf')
  //   cy.get('.v-list-item__title > .v-list-item__content').should('length', 0)
  //   cy.get('input').should('exist').clear()
  // })

  // it('should display variety information', () => {
  //   cy.get('.v-list-item__title > .v-list-item__content').first().click()
  //   cy.get('.variety').first().click()
  //   cy.get('.v-dialog input').eq(2).should('have.value', '1')
  //   cy.get('.v-dialog input').eq(3).should('have.value', 'first variety nameサイズ')
  //   cy.get('.v-dialog input').eq(4).should('have.value', 'first short name')
  //   cy.get('.v-dialog input').eq(5).should('have.value', 'first variety yomiサイズ')
  //   cy.get('.v-dialog input').eq(6).should('have.value', 'first name eng')
  //   cy.get('i.mdi-close').click()
  // })

  // it('should success create new variety', () => {
  //   cy.wait(200)
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-plus').click()
  //   cy.get('.v-select__selections').click()
  //   cy.get('.v-list-item__content').contains(items[0].name).click()
  //   cy.get('.v-dialog input').eq(3).type(newVariety.name)
  //   cy.get('.v-dialog input').eq(4).type(newVariety.short_name)
  //   cy.get('.v-dialog input').eq(6).type(newVariety.name_eng)
  //   const newVarietiesByItem = varietiesByItem
  //   newVarietiesByItem[0].varieties.push(newVariety)

  //   cy.intercept('GET', '/varieties/group_by_item', { body: newVarietiesByItem })
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.wait('@createVariety').its('request.body').should('deep.equal', {
  //     item: newVariety.item.id,
  //     name: newVariety.name,
  //     yomi: newVariety.yomi,
  //     name_eng: newVariety.name_eng,
  //     short_name: newVariety.short_name
  //   })
  //   cy.get('i.v-icon.mdi-close').click()
  //   cy.get('.v-list-item__title > .v-list-item__content').first().click()
  //   cy.get('.variety').should('length', 3)
  //   cy.get('.variety').eq(2).should('contain', 'fifth variety name')
  // })

  // it('should fill yomi automatically', () => {
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-plus').click()
  //   cy.get('.v-dialog input').eq(3).type(newVariety.name)
  //   cy.wait('@toYomi')
  //   cy.get('.v-dialog input').eq(5).should('have.value', newVariety.name)
  //   cy.get('i.mdi-close').click()
  // })

  // it('should fail create new variety when name empty', () => {
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-plus').click()
  //   cy.get('.v-dialog input').eq(3).type(newVarietyNameEmpty.name)
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('.v-dialog input').eq(3).should('be.empty')
  //   cy.get('.Vue-Toastification__toast-body').should('contain', 'Can not save, name is empty')
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('i.mdi-close').click()
  //   cy.get('.v-list-item__title > .v-list-item__content').first().click()
  //   cy.get('.variety').should('length', 3)
  // })

  // it('should fail create new variety when name exits', () => {
  //   cy.wait(500)
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-plus').click()
  //   cy.get('.v-select__selections').click()
  //   cy.get('.v-list-item__content').contains(items[0].name).click()
  //   cy.get('.v-dialog input').eq(3).type(newVariety.name)
  //   cy.get('.v-dialog input').eq(4).type(newVariety.short_name)
  //   cy.get('.v-dialog input').eq(5).type(newVariety.name_eng)

  //   cy.intercept('POST', '/varieties', {
  //     body: { messages: ['Name is already existed'] },
  //     statusCode: 400
  //   }).as('postNameExits')
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.wait('@postNameExits')
  //   cy.get('div.Vue-Toastification__toast-body').should('contain', 'Name is already existed')
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('i.mdi-close').click()
  //   cy.get('.variety').should('length', 3)
  // })

  // it('should show dialog when sorting', () => {
  //   cy.wait(500)
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-sort-ascending').click()
  //   cy.get('.v-bottom-sheet').should('be.visible')
  //   cy.get('span.v-btn__content').contains('Sort ascending by name').click()
  //   cy.get('.v-dialog > .v-card > .v-card__title').should('contain', 'Sort ascending by name')
  // })

  // it('should not save sort by name when close', () => {
  //   cy.get('.light_red > .v-btn__content').click()
  //   cy.get('.variety').should(($span) => {
  //     expect($span).to.have.length(3)
  //     expect($span.eq(0)).to.contain('first variety nameサイズ')
  //     expect($span.eq(1)).to.contain('second variety name')
  //     expect($span.eq(2)).to.contain('fifth variety name')
  //   })
  //   cy.get('.v-toolbar__title').should('not.be.enabled')
  // })

  // it('should save sort chosen item by name', () => {
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-sort-ascending').click()
  //   cy.get('span').contains('Sort ascending by name').click()
  //   cy.get('.v-input--radio-group__input >').eq(1).click()
  //   cy.get('.row > .rough_black > .v-btn__content').click()
  //   cy.wait('@sortVariety').its('request.body').should('deep.equal', orderOne)
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('.v-toolbar__title').should('not.be.enabled')
  // })

  // it('should save sort all by name', () => {
  //   cy.wait(100)
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-sort-ascending').click()
  //   cy.get('span').contains('Sort ascending by name').click()
  //   cy.get('.v-input--radio-group__input >').eq(0).click()
  //   cy.get('.row > .rough_black > .v-btn__content').click()
  //   cy.wait('@sortVariety').its('request.body').should('deep.equal', orderAll)
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('.v-toolbar__title').should('not.be.enabled')
  // })

  // it('should fail to update name already exists', () => {
  //   cy.get('.v-list-item__title > .v-list-item__content').eq(1).click()
  //   cy.get('.variety').contains('third variety name').click()
  //   cy.get('.v-dialog input').eq(3).clear().type(varietiesByItem[0].varieties[0].name)

  //   cy.intercept('PUT', `/varieties/${updateVariety.id}`, {
  //     body: { messages: ['Name is already existed'] },
  //     statusCode: 400
  //   }).as('updateFailed')

  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.wait('@updateFailed').its('request.body').should('contain', {
  //     name: varietiesByItem[0].varieties[0].name
  //   })

  //   cy.get('div.Vue-Toastification__toast-body').should('contain', 'Name is already existed')
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('i.v-icon.mdi-close').first().click()
  //   cy.get('.v-list-item__title > .v-list-item__content').eq(1).click()
  // })

  // it('should fail to update name already exists (with space)', () => {
  //   cy.get('.v-list-item__title > .v-list-item__content').eq(1).click()
  //   cy.get('.variety').contains('third variety name').click()
  //   cy.get('.v-dialog input').eq(3).clear().type(`${varietiesByItem[0].varieties[0].name}    `)

  //   cy.intercept('PUT', `/varieties/${updateVariety.id}`, {
  //     body: { messages: ['Name is already existed'] },
  //     statusCode: 400
  //   }).as('updateFailed')

  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.wait('@updateFailed')
  //     .its('request.body')
  //     .should('contain', {
  //       name: `${varietiesByItem[0].varieties[0].name}`
  //     })

  //   cy.get('div.Vue-Toastification__toast-body').should('contain', 'Name is already existed')
  //   cy.get('button.Vue-Toastification__close-button').click({ multiple: true })
  //   cy.get('i.v-icon.mdi-close').first().click()
  //   cy.get('.v-list-item__title > .v-list-item__content').eq(1).click()
  // })

  // it('should fail to update name already exists (half width)', () => {
  //   cy.get('.v-list-item__title > .v-list-item__content').eq(1).click()
  //   cy.get('.variety').contains('third variety name').click()
  //   cy.get('.v-dialog input').eq(3).clear().type('first variety nameｻｲｽﾞ')

  //   cy.intercept('PUT', `/varieties/${updateVariety.id}`, {
  //     body: { messages: ['Name is already existed'] },
  //     statusCode: 400
  //   }).as('updateFailed')

  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.wait('@updateFailed').its('request.body').should('contain', {
  //     name: 'first variety nameｻｲｽﾞ'
  //   })

  //   cy.get('div.Vue-Toastification__toast-body').should('contain', 'Name is already existed')
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('i.mdi-close').first().click()
  //   cy.get('.v-list-item__title > .v-list-item__content').eq(1).click()
  // })

  // it('should success to update variety', () => {
  //   cy.get('.v-list-item__title > .v-list-item__content').eq(1).click()
  //   cy.get('.variety').contains('third variety name').click()
  //   cy.get('.v-dialog input').eq(6).clear().type(updateVariety.name_eng)

  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.wait('@updateVariety').its('request.body').should('deep.equal', {
  //     name: updateVariety.name,
  //     name_eng: updateVariety.name_eng,
  //     short_name: updateVariety.short_name,
  //     yomi: updateVariety.yomi,
  //     item: updateVariety.item.id
  //   })

  //   cy.get('div.Vue-Toastification__toast-body').should('contain', 'Update successfully')
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('.v-list-item__title > .v-list-item__content').eq(1).click()
  // })

  // it('should cancel delete', () => {
  //   cy.get('.variety').contains('fifth variety name').click()
  //   cy.get('.light_red').contains('Delete').click()
  //   cy.get('span.blue--text').contains('キャンセル').click()
  //   cy.get('i.v-icon.mdi-close').first().click()
  //   cy.get('.variety').contains('fifth variety name').should('exist')
  //   cy.get('.v-list-item__title > .v-list-item__content').eq(0).click()
  // })

  // it('should fail to delete variety already used in an Order detail', () => {
  //   cy.get('.v-list-item__title > .v-list-item__content').eq(0).click()
  //   cy.get('.variety').contains('fifth variety name').click()

  //   cy.intercept('DELETE', `/varieties/${newVariety.id}`, {
  //     body: {
  //       messages: [`Can not delete. This variety is used in Order detail: ID = 177`]
  //     },
  //     statusCode: 400
  //   }).as('deleteFailed')

  //   cy.get('.light_red').contains('Delete').click()
  //   cy.get('span.red--text').contains('Delete').click()
  //   cy.wait('@deleteFailed')
  //   cy.get('div.Vue-Toastification__toast-body').should(
  //     'contain',
  //     'Can not delete. This variety is used in Order detail: ID = 177'
  //   )
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('.variety').contains('fifth variety name').should('exist')
  //   cy.get('.v-list-item__title > .v-list-item__content').eq(0).click()
  // })

  // it('should fail to delete variety already used in an Packing result', () => {
  //   cy.get('.v-list-item__title > .v-list-item__content').eq(0).click()
  //   cy.get('.variety').contains('fifth variety name').click()

  //   cy.intercept('DELETE', `/varieties/${newVariety.id}`, {
  //     body: {
  //       messages: [`Can not delete. This variety is used in Packing result: ID = 177`]
  //     },
  //     statusCode: 400
  //   }).as('deleteFailed')

  //   cy.get('.light_red').contains('Delete').click()
  //   cy.get('span.red--text').contains('Delete').click()
  //   cy.wait('@deleteFailed')
  //   cy.get('div.Vue-Toastification__toast-body').should(
  //     'contain',
  //     'Can not delete. This variety is used in Packing result: ID = 177'
  //   )
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('.variety').contains('fifth variety name').should('exist')
  //   cy.get('.v-list-item__title > .v-list-item__content').eq(0).click()
  // })

  // it('should success to delete variety', () => {
  //   cy.get('.v-list-item__title > .v-list-item__content').eq(0).click()
  //   cy.get('.variety').contains('fifth variety name').click()
  //   cy.get('.light_red').contains('Delete').click()
  //   cy.get('span.red--text').contains('Delete').click()
  //   cy.wait('@deleteVariety')
  //   cy.get('div.Vue-Toastification__toast-body').should('contain', 'Delete successfully')
  //   cy.get('.v-list-item__title > .v-list-item__content').eq(0).click()
  // })
})
