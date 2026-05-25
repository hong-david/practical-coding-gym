# 021 Frontend Cart Component

## Goal

Build a real frontend component/state lab with JavaScript tooling. The exercise is to implement a shopping-cart state store and DOM component with loading, error, optimistic update, and accessibility behavior.

## Files to Implement

```txt
package.json
src/
    cartStore.js
    cartComponent.js
fixtures/
    cart.json
tests/
    provided/
        cartComponent.test.js
    custom/
```

## API/functions/classes expected

```javascript
createCartStore(initialState)
cartReducer(state, action)
calculateTotals(items)
loadCart(api, store)
saveCart(api, store)
renderCart({ root, store, api })
```

## Input/output shape

Cart state includes `items`, `loading`, `error`, `saving`, and `lastSavedAt`. Items include `id`, `name`, `price`, and `quantity`. The DOM component should render cart rows, totals, quantity controls, loading/error states, and accessible buttons.

## Level 1 MVP

Implement reducer-driven cart state, render items into the DOM, calculate totals, and handle quantity updates.

## Level 2 Edge Cases

Handle empty carts, invalid quantities, price precision, failed API loads/saves, optimistic update rollback, disabled controls while saving, DOM rerendering without leaks, and mutation-safe state transitions.

## Level 3 Senior Follow-Ups

Add keyboard shortcuts, focus management, offline retry, localStorage persistence, debounced saves, integration with a real framework, and visual regression tests.

## Provided test command

```bash
cd problems/021-frontend-cart-component
npm install
npm test
```

## Custom test command

```bash
cd problems/021-frontend-cart-component
npm test -- tests/custom
```

## Manual run command

```bash
cd problems/021-frontend-cart-component
npm test
```

## Definition of Done

Provided JS tests pass, meaningful custom tests pass, the component behaves correctly in jsdom, and state changes are mutation-safe.

## PR Review Checklist

Check reducer purity, DOM accessibility, loading/error states, API failure behavior, optimistic update rollback, event listener cleanup, price handling, test readability, and whether UI state is separated from rendering.
