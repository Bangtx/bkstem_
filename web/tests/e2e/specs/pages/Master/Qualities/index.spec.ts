describe('Master quality page', () => {
  const qualities = [
    {
      name: 'first quality name',
      name_eng: 'test',
      short_name: 'short name',
      yomi: 'yomi',
      id: 1,
      order_num: 1,
      search_str: 'first quality nameサイズyomitest',
      active: true,
      created_at: '2021-05-26',
      created_by: null
    },
    {
      name: 'second quality name',
      name_eng: 'name eng',
      short_name: 'short name',
      yomi: null,
      id: 2,
      order_num: 2,
      search_str: 'second quality name box l',
      active: true,
      created_at: '2021-05-26',
      created_by: null
    }
  ]

  const newQuality = {
    name: 'third quality name',
    name_eng: 'name eng',
    short_name: 'short name',
    yomi: 'yomi',
    id: 3,
    order_num: 3,
    search_str: 'third quality name',
    active: true,
    created_at: '2021-05-26',
    created_by: null
  }

  // const newQualityNameEmpty = {
  //   name: '    ',
  //   name_eng: 'name eng',
  //   short_name: 'short name',
  //   yomi: '',
  //   id: 4,
  //   order_num: 4,
  //   search_str: 'quality with name empty',
  //   active: true,
  //   created_at: '2021-05-28',
  //   created_by: null
  // }

  // const updateQuality = {
  //   name: 'third quality name update',
  //   name_eng: 'name eng update',
  //   short_name: 'short name',
  //   yomi: 'yomi',
  //   id: 3,
  //   order_num: 3,
  //   search_str: 'third quality name',
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
    cy.intercept('GET', '/qualities', { body: qualities }).as('getQualities')

    cy.intercept('POST', '/qualities', {
      body: newQuality,
      statusCode: 200
    }).as('createQuality')

    cy.intercept('PUT', `/qualities/${newQuality.id}`, { body: newQuality, statusCode: 200 }).as(
      'updateQuality'
    )

    cy.intercept('DELETE', `/qualities/${newQuality.id}`, {
      response: newQuality.id,
      statusCode: 200
    })

    cy.intercept('POST', '/qualities/sort', {
      statusCode: 200,
      body: { detail: 'Sort Quality' }
    }).as('sortQuality')
    cy.intercept(
      {
        pathname: '/common/get-pronunciation',
        query: {
          text: newQuality.name
        }
      },
      { statusCode: 200, body: newQuality.name }
    ).as('toYomi')
  })

  it('should display list quality', () => {
    cy.visit('/master/qualities')
    cy.wait('@getQualities')

    cy.get('.v-list-item > span').should(($span) => {
      expect($span).to.have.length(2)
      expect($span.eq(0)).to.contain('first quality name')
      expect($span.eq(1)).to.contain('second quality name')
    })
  })

  it('should display search quality by name', () => {
    cy.get('input').should('exist').type('first')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first quality name')

    cy.get('input').should('exist').clear()
    cy.get('.v-list-item > span').should('length', 2)

    cy.get('input').should('exist').type('second')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'second quality name')
  })

  it('should search quality by yomi', () => {
    cy.get('input').should('exist').clear().type('yomi')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first quality name')
  })

  it('should search quality by name eng', () => {
    cy.get('input').should('exist').clear().type('test')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first quality name')
  })

  it('should search quality with upper characters', () => {
    cy.get('input').should('exist').clear().type('BOX L')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'second quality name')
  })

  it('should search quality by half width', () => {
    cy.get('input').should('exist').clear().type('ｻｲｽﾞ')
    cy.get('.v-list-item > span').should('length', 1).should('contain', 'first quality name')
  })

  it('should search quality render empty', () => {
    cy.get('input').should('exist').type('abcxyz')
    cy.get('.v-list-item > span').should('length', 0)
    cy.get('input').should('exist').clear()
  })

  it('should display quality information', () => {
    cy.get('.v-list-item > span').first().click()
    cy.get('.v-dialog input:first').should('have.value', 'first quality name')
    cy.get('.v-dialog input').eq(1).should('have.value', 'yomi')
    cy.get('.v-dialog input').eq(2).should('have.value', 'test')
    cy.get('i.mdi-close').click()
  })

  // it('should success create new quality', () => {
  //   cy.wait(200)
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-plus').click()
  //   cy.get('.v-dialog input').eq(0).type(newQuality.name)
  //   cy.get('.v-dialog input').eq(1).should('have.value', newQuality.name)
  //   cy.get('.v-dialog input').eq(1).clear().type(newQuality.yomi)
  //   cy.get('.v-dialog input').eq(2).type(newQuality.name_eng)
  //   cy.get('.v-dialog input').eq(3).type(newQuality.short_name)

  //   cy.intercept('GET', '/qualities', { body: [...qualities, newQuality] })
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.wait('@createQuality').its('request.body').should('deep.equal', {
  //     name: newQuality.name,
  //     name_eng: newQuality.name_eng,
  //     short_name: newQuality.short_name,
  //     yomi: newQuality.yomi
  //   })
  //   cy.get('.v-list-item > span').should('length', 3)
  //   cy.get('.v-list-item > span').eq(2).should('contain', 'third quality name')
  //   cy.get('i.mdi-close').click()
  // })

  // it('should fail create new quality when name empty', () => {
  //   cy.wait(200)
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-plus').click()
  //   cy.get('.v-dialog input').eq(0).type(newQualityNameEmpty.name)
  //   cy.get('.v-dialog input').eq(2).type(newQualityNameEmpty.name_eng)
  //   cy.get('.v-dialog input').eq(3).type(newQualityNameEmpty.short_name)
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('.v-dialog input').eq(0).should('be.empty')
  //   cy.get('.v-dialog input').eq(1).should('be.empty')
  //   cy.get('.Vue-Toastification__toast-body').should('contain', 'Cannot save, name is empty')
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('i.mdi-close').click()
  //   cy.get('.v-list-item > span').should('length', 3)
  // })

  // it('should fail create new quality when name exits', () => {
  //   cy.wait(500)
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-plus').click()
  //   cy.get('.v-dialog input').eq(0).type(newQuality.name)
  //   cy.get('.v-dialog input').eq(1).clear().type(newQuality.yomi)
  //   cy.get('.v-dialog input').eq(2).clear().type(newQuality.name_eng)
  //   cy.get('.v-dialog input').eq(3).clear().type(newQuality.short_name)

  //   cy.intercept('POST', '/qualities', {
  //     body: { messages: ['Name is already existed'] },
  //     statusCode: 400
  //   })
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('div.Vue-Toastification__toast-body').should('contain', 'Name is already existed')
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('i.mdi-close').click()
  //   cy.get('.v-list-item > span').should('length', 3)
  // })

  // it('should success update quality', () => {
  //   cy.get('.v-list-item > span').eq(2).click()
  //   cy.get('.v-dialog input:first').clear().type(updateQuality.name)
  //   cy.get('.v-dialog input').eq(1).clear().type(updateQuality.yomi)
  //   cy.get('.v-dialog input').eq(2).clear().type(updateQuality.name_eng)
  //   cy.get('.v-dialog input').eq(3).clear().type(updateQuality.short_name)

  //   cy.intercept('GET', '/qualities', { body: [...qualities, updateQuality] })
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.wait('@updateQuality').its('request.body').should('deep.equal', {
  //     name: updateQuality.name,
  //     name_eng: updateQuality.name_eng,
  //     short_name: updateQuality.short_name,
  //     yomi: updateQuality.yomi
  //   })
  //   cy.get('.v-list-item > span').eq(2).should('contain', updateQuality.name)
  // })

  // it('should fail update quality name exits', () => {
  //   cy.get('.v-list-item > span').eq(2).click()
  //   cy.get('.v-dialog input:first').clear().type(updateQuality.name)
  //   cy.get('.v-dialog input').eq(1).clear().type(updateQuality.yomi)
  //   cy.get('.v-dialog input').eq(2).clear().type(updateQuality.name_eng)
  //   cy.get('.v-dialog input').eq(3).clear().type(updateQuality.short_name)

  //   cy.intercept('PUT', `/qualities/${newQuality.id}`, {
  //     body: { messages: ['Name is already existed'] },
  //     statusCode: 400
  //   })
  //   cy.get('span.v-btn__content').contains('Save').click()
  //   cy.get('div.Vue-Toastification__toast-body').should('contain', 'Name is already existed')
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('i.mdi-close').click()
  // })

  // it('should success delete quality', () => {
  //   cy.wait(500)
  //   cy.get('.v-list-item > span').eq(2).click()
  //   cy.get('span').contains('Delete').click()
  //   cy.get('span.red--text').contains('Delete').click()
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('.v-list-item > span').should('length', 2)
  // })

  // it('should fail delete quality when cancel', () => {
  //   cy.wait(500)
  //   cy.get('.v-list-item > span').eq(1).click()
  //   cy.get('.light_red').contains('Delete').click()
  //   cy.get('span.blue--text').contains('キャンセル').click()
  //   cy.get('.v-card__title').contains('Edit quality').should('length', 1)
  //   cy.get('i.mdi-close').click()
  //   cy.get('.v-list-item > span').should('length', 2)
  // })

  // it('should fail delete quality when it is used in order', () => {
  //   cy.get('.v-list-item > span').eq(1).click()
  //   cy.get('.light_red').contains('Delete').click()

  //   cy.intercept('DELETE', `/qualities/${qualities[1].id}`, {
  //     body: {
  //       messages: [`Can not delete. This quality is used in Order detail: ID=${qualities[1].id}`]
  //     },
  //     statusCode: 400
  //   })
  //   cy.get('span.red--text').contains('Delete').click()
  //   cy.get('.Vue-Toastification__toast-body').contains(
  //     'Can not delete. This quality is used in Order detail: ID=2'
  //   )
  //   cy.wait(500)
  //   cy.get('button.Vue-Toastification__close-button').click({ multiple: true })
  //   cy.get('i.mdi-close').click()
  //   cy.get('.v-list-item > span').should('length', 2)
  // })

  // it('should sort by name and show info message, buttons', () => {
  //   cy.wait(1000)
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-sort-ascending').click()
  //   cy.get('.v-bottom-sheet').should('be.visible')
  //   cy.get('span.v-btn__content').contains('Sort ascending by name').click()
  //   cy.get('span').contains('Quality list is sorted').should('be.visible')
  //   cy.get('span').contains('Click [Save] button on the top right to save').should('be.visible')
  //   cy.get('.v-list-item > span').should(($span) => {
  //     expect($span.eq(0)).to.contain('first quality name')
  //     expect($span.eq(1)).to.contain('second quality name')
  //   })
  //   cy.get('i.mdi-close').should('be.visible')
  //   cy.get('i.mdi-content-save').should('be.visible')
  // })

  // it('should cancel sort by name and hide info message, buttons', () => {
  //   cy.wait(150)
  //   cy.get('i.mdi-close').first().click()
  //   cy.get('i.mdi-close').should('not.be.visible')
  //   cy.get('i.mdi-content-save').should('not.exist')
  //   cy.get('span').contains('Quality list is sorted').should('not.exist')
  //   cy.get('span').contains('Click [Save] button on the top right to save').should('not.exist')
  // })

  // it('should save sort by name order and hide info message, buttons', () => {
  //   cy.get('i.mdi-dots-vertical').click()
  //   cy.get('i.mdi-sort-ascending').click()
  //   cy.get('span.v-btn__content').contains('Sort ascending by name').click()
  //   cy.get('i.mdi-content-save').click()
  //   cy.wait('@sortQuality').its('request.body').should('deep.equal', order)
  //   cy.get('.Vue-Toastification__toast-body').should('contain', 'Save order successful')
  //   cy.get('button.Vue-Toastification__close-button').click()
  //   cy.get('i.mdi-close').should('not.be.visible')
  //   cy.get('i.mdi-content-save').should('not.exist')
  //   cy.get('span').contains('Quality list is sorted').should('not.exist')
  //   cy.get('span').contains('Click [Save] button on the top right to save').should('not.exist')
  //   cy.get('.v-list-item > span').should(($span) => {
  //     expect($span.eq(0)).to.contain('first quality name')
  //     expect($span.eq(1)).to.contain('second quality name')
  //   })
  // })
})
