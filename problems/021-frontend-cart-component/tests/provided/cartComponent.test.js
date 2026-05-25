const {
  createCartStore,
  cartReducer,
  calculateTotals,
  loadCart,
  saveCart
} = require("../../src/cartStore");
const { renderCart } = require("../../src/cartComponent");

function initialState(overrides = {}) {
  return {
    items: [],
    loading: false,
    error: null,
    saving: false,
    lastSavedAt: null,
    ...overrides
  };
}

function item(overrides = {}) {
  return {
    id: "sku-1",
    name: "Keyboard",
    price: "99.99",
    quantity: 1,
    ...overrides
  };
}

describe("cartReducer", () => {
  test("initializes with empty cart shape", () => {
    const store = createCartStore();
    expect(store.getState()).toMatchObject(initialState());
  });

  test("load_started sets loading and clears error", () => {
    const state = cartReducer(initialState({ error: "bad" }), { type: "load_started" });
    expect(state.loading).toBe(true);
    expect(state.error).toBe(null);
  });

  test("load_succeeded stores items", () => {
    const state = cartReducer(initialState({ loading: true }), { type: "load_succeeded", items: [item()] });
    expect(state.items).toHaveLength(1);
    expect(state.loading).toBe(false);
  });

  test("load_failed stores error", () => {
    const state = cartReducer(initialState({ loading: true }), { type: "load_failed", error: "network" });
    expect(state.error).toBe("network");
    expect(state.loading).toBe(false);
  });

  test("quantity_changed updates matching item only", () => {
    const state = cartReducer(initialState({ items: [item(), item({ id: "sku-2" })] }), {
      type: "quantity_changed",
      itemId: "sku-1",
      quantity: 3
    });
    expect(state.items.map((cartItem) => cartItem.quantity)).toEqual([3, 1]);
  });

  test("quantity_changed rejects quantity below one", () => {
    expect(() => cartReducer(initialState({ items: [item()] }), {
      type: "quantity_changed",
      itemId: "sku-1",
      quantity: 0
    })).toThrow();
  });

  test("remove_item removes matching item", () => {
    const state = cartReducer(initialState({ items: [item(), item({ id: "sku-2" })] }), {
      type: "remove_item",
      itemId: "sku-1"
    });
    expect(state.items.map((cartItem) => cartItem.id)).toEqual(["sku-2"]);
  });

  test("unknown action throws", () => {
    expect(() => cartReducer(initialState(), { type: "wat" })).toThrow();
  });

  test("reducer does not mutate input state", () => {
    const state = initialState({ items: [item()] });
    cartReducer(state, { type: "quantity_changed", itemId: "sku-1", quantity: 2 });
    expect(state.items[0].quantity).toBe(1);
  });
});

describe("cart totals and API helpers", () => {
  test("calculateTotals returns item count and subtotal", () => {
    expect(calculateTotals([item({ price: "10.00", quantity: 2 })])).toEqual({
      itemCount: 2,
      subtotal: "20.00"
    });
  });

  test("calculateTotals handles decimal precision", () => {
    expect(calculateTotals([item({ price: "0.10", quantity: 3 })]).subtotal).toBe("0.30");
  });

  test("calculateTotals rejects negative price", () => {
    expect(() => calculateTotals([item({ price: "-1.00" })])).toThrow();
  });

  test("loadCart dispatches loaded items", async () => {
    const store = createCartStore();
    const api = { fetchCart: jest.fn().mockResolvedValue({ items: [item()] }) };
    await loadCart(api, store);
    expect(store.getState().items).toHaveLength(1);
  });

  test("loadCart stores API errors", async () => {
    const store = createCartStore();
    const api = { fetchCart: jest.fn().mockRejectedValue(new Error("down")) };
    await expect(loadCart(api, store)).rejects.toThrow("down");
    expect(store.getState().error).toMatch(/down/);
  });

  test("saveCart marks lastSavedAt on success", async () => {
    const store = createCartStore(initialState({ items: [item()] }));
    const api = { saveCart: jest.fn().mockResolvedValue({ savedAt: "2026-05-01T10:00:00Z" }) };
    await saveCart(api, store);
    expect(store.getState().lastSavedAt).toBe("2026-05-01T10:00:00Z");
  });
});

describe("renderCart", () => {
  test("renders empty cart state", () => {
    document.body.innerHTML = '<main id="root"></main>';
    const store = createCartStore();
    renderCart({ root: document.getElementById("root"), store, api: {} });
    expect(document.body.textContent).toMatch(/empty/i);
  });

  test("renders item rows and total", () => {
    document.body.innerHTML = '<main id="root"></main>';
    const store = createCartStore(initialState({ items: [item({ price: "10.00", quantity: 2 })] }));
    renderCart({ root: document.getElementById("root"), store, api: {} });
    expect(document.body.textContent).toMatch(/Keyboard/);
    expect(document.body.textContent).toMatch(/20.00/);
  });

  test("quantity buttons have accessible names", () => {
    document.body.innerHTML = '<main id="root"></main>';
    const store = createCartStore(initialState({ items: [item()] }));
    renderCart({ root: document.getElementById("root"), store, api: {} });
    expect(document.querySelector('button[aria-label="Increase Keyboard quantity"]')).not.toBeNull();
    expect(document.querySelector('button[aria-label="Decrease Keyboard quantity"]')).not.toBeNull();
  });

  test("clicking increase updates quantity", () => {
    document.body.innerHTML = '<main id="root"></main>';
    const store = createCartStore(initialState({ items: [item()] }));
    renderCart({ root: document.getElementById("root"), store, api: {} });
    document.querySelector('button[aria-label="Increase Keyboard quantity"]').click();
    expect(store.getState().items[0].quantity).toBe(2);
  });

  test("saving state disables buttons", () => {
    document.body.innerHTML = '<main id="root"></main>';
    const store = createCartStore(initialState({ items: [item()], saving: true }));
    renderCart({ root: document.getElementById("root"), store, api: {} });
    expect(document.querySelector("button").disabled).toBe(true);
  });

  test("error state renders alert", () => {
    document.body.innerHTML = '<main id="root"></main>';
    const store = createCartStore(initialState({ error: "network" }));
    renderCart({ root: document.getElementById("root"), store, api: {} });
    expect(document.querySelector('[role="alert"]').textContent).toMatch(/network/);
  });
});
