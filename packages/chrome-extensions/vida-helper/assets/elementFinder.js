// @ts-check

(function () {
  'use strict'

  console.log('elementFinder.js loaded')
  // getEventListeners 这个函数只有在 devtool 里面有，外面拿不到，所以用不了
  console.log('has getEventListeners?', /** @type {any}*/(window).getEventListeners)

  const clickableTagNames = new Set([
    'a',
    'button',
    'details',
    'embed',
    'input',
    'label',
    'menu',
    'menuitem',
    'object',
    'select',
    'textarea',
    'summary',
  ])

  const clickableRoleValues = new Set([
    'button',
    'tab',
    'link',
    'checkbox',
    'menuitem',
    'menuitemcheckbox',
    'menuitemradio',
    'radio',
  ])

  const elementBlacklist = new Set(['svg', 'script', 'style', 'link', 'meta'])

  /**
   * Generates a unique CSS selector for a DOM element
   * @param {HTMLElement} element - The DOM element to generate a selector for
   * @returns {string} A CSS selector that uniquely identifies the element
   */
  function getSelector(element) {
    if (!element) return ''

    const original = element
    const paths = []

    while (
      element &&
      element.nodeType === Node.ELEMENT_NODE &&
      element.tagName !== 'BODY'
    ) {
      let selector = element.tagName.toLowerCase()
      let index = 1
      /** @type {Element | null} */
      let sibling = element.previousElementSibling

      while (sibling) {
        if (sibling.tagName === element.tagName) {
          index++
        }
        sibling = sibling.previousElementSibling
      }

      if (index > 1 || element.nextElementSibling?.tagName === element.tagName) {
        selector += `:nth-of-type(${index})`
      }

      paths.unshift(selector)
      element = /** @type {HTMLElement} */ (element.parentNode)
    }

    const selector = 'body > ' + paths.join(' > ')

    // Verify selector points to original element
    if (document.querySelector(selector) !== original) {
      console.error('selector not match', selector, original)
      return ''
    }

    return selector
  }

  /**
   * Gets all visible elements in the document that match the selector
   * @returns {Promise<HTMLElement[]>} Promise that resolves to an array of visible elements
   */
  function getAllVisibleElements() {
    /** @type {Set<HTMLElement>} */
    const visibleElements = new Set()

    /**
     * Checks if an element is actually visible based on its computed style
     * @param {Element} element - The element to check
     * @returns {boolean} True if the element is visible
     */
    function isActuallyVisible(element) {
      if (!(element instanceof HTMLElement)) {
        return false
      }
      if (element.offsetHeight === 0 || element.offsetWidth === 0) {
        return false
      }
      const style = window.getComputedStyle(element)
      return style.visibility !== 'hidden' &&
        style.opacity !== '0' &&
        style.display !== 'none'
    }

    /**
     * Gets all elements that match the selector within a root element
     * @param {Document | DocumentFragment} root - The root element to search within
     * @returns {Element[]} Array of matching elements
     */
    function getAllElements(root) {
      return Array.from(root.querySelectorAll('*'))
    }

    return new Promise((resolve) => {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && isActuallyVisible(entry.target)) {
            visibleElements.add(/** @type {HTMLElement} */(entry.target))
          } else {
            visibleElements.delete(/** @type {HTMLElement} */(entry.target))
          }
        })

        setTimeout(() => {
          observer.disconnect()
          resolve(Array.from(visibleElements))
        }, 0)
      })

      getAllElements(document).forEach(el => observer.observe(el))
    })
  }

  /**
   * Detects and reports all clickable elements in the document
   * @returns {void}
   */
  function getClickableElements() {
    /**
     * Checks if an element has click-related event listeners
     * @param {HTMLElement} element - The element to check for click events
     * @returns {{isClickable: boolean, reason?: string}}
     */
    function isClickable(element) {
      if (element.tagName === 'body') {
        return { isClickable: false, reason: 'isBody' }
      }

      const tagName = element.tagName.toLowerCase()

      if (clickableTagNames.has(tagName)) {
        return { isClickable: true, reason: 'tagName' }
      }

      if (elementBlacklist.has(tagName)) {
        return { isClickable: false, reason: 'blacklist' }
      }

      const role = element.getAttribute('role')
      if (role && clickableRoleValues.has(role)) {
        return { isClickable: true, reason: 'role' }
      }

      const ariaRole = element.getAttribute('aria-role')
      if (ariaRole && clickableRoleValues.has(ariaRole)) {
        return { isClickable: true, reason: 'ariaRole' }
      }
      // tabIndex 如果要支持的话需要做更细致的处理，vimium 的处理是只有他和别的元素不重叠的时候才显示
      // const tabIndex = element.getAttribute('tabindex')

      // Add check for specific class
      const hasAddressInputClass = element.classList.contains(
        'address-input__container__input',
      )

      // Basic role/attribute checks
      const hasInteractiveRole =
        hasAddressInputClass ||
        // (tabIndex !== null &&
        //   tabIndex !== '-1' &&
        //   element.parentElement?.tagName.toLowerCase() !== 'body') ||
        element.getAttribute('data-action') === 'a-dropdown-select' ||
        element.getAttribute('data-action') === 'a-dropdown-button'

      if (hasInteractiveRole) {
        return { isClickable: true, reason: 'interactiveRole' }
      }

      // Check inline handlers
      if (element.onclick !== null ||
        element.getAttribute('onclick') !== null ||
        element.hasAttribute('ng-click') ||
        element.hasAttribute('@click') ||
        element.hasAttribute('v-on:click')) {
        return { isClickable: true, reason: 'inlineHandler' }
      }

      /** @type {any} */
      const win = window
      // Check event listeners using Chrome DevTools API
      /** @type {Record<string, {listener: Function, useCapture: boolean}[]>} */
      const listeners = win.getEventListeners?.(element) || {}
      console.log('listeners', listeners)
      const hasListener = listeners.click?.length > 0 ||
        listeners.mousedown?.length > 0 ||
        listeners.mouseup?.length > 0 ||
        listeners.touchstart?.length > 0 ||
        listeners.touchend?.length > 0
      if (hasListener) {
        return { isClickable: true, reason: 'listener' }
      }
      return { isClickable: false }
    }

    getAllVisibleElements().then(elements => {
      console.log('visible elements', elements)
      /**
       * @type {Array<[string, string]>}
       */
      const clickableElements = elements
        .flatMap(element => {
          const res = isClickable(element)
          console.log('clickable res', element, res)
          if (res.isClickable) {
            return [[getSelector(element), res.reason || '']]
          }
          return []
        })

      // Send message back to extension
      window.postMessage({
        type: 'CLICKABLE_ELEMENTS_DETECTED',
        elements: clickableElements
      }, window.origin)
    }).catch((err) => {
      console.error(err)
    })
  }

  // Listen for messages from the extension
  window.addEventListener('message', (/** @type {MessageEvent} */ event) => {
    if (event.data.type === 'DETECT_CLICKABLE_ELEMENTS') {
      console.log('run detect')
      getClickableElements()
    }
  })
})