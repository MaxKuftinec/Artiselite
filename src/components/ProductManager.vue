<template>
  <div>
    <v-form v-model="valid">
      <v-text-field
        v-model="newProduct.name"
        label="Product Name"
        required
      ></v-text-field>

      <v-text-field
        v-model="newProduct.quantity"
        label="Quantity"
        type="number"
        required
      ></v-text-field>

      <v-btn @click="addProduct" :disabled="!valid">Add Product</v-btn>
    </v-form>

    <v-data-table
      :headers="headers"
      :items="products"
      item-key="name"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Products</v-toolbar-title>
        </v-toolbar>
      </template>
    </v-data-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      valid: false,
      newProduct: {
        name: '',
        quantity: 0,
      },
      products: [],
      headers: [
        { text: 'Name', value: 'name' },
        { text: 'Quantity', value: 'quantity' },
      ],
    };
  },
  methods: {
    addProduct() {
      if (this.newProduct.name && this.newProduct.quantity > 0) {
        this.products.push({ ...this.newProduct });
        this.newProduct.name = '';
        this.newProduct.quantity = 0;
      }
    },
  },
};
</script>
