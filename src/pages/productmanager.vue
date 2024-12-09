<template>
  <v-app>
    <v-container>
      <v-card>
        <v-card-title>Warehouse Inventory Management</v-card-title>
        <v-card-text>
          <product-manager />
        </v-card-text>
      </v-card>
    </v-container>
  </v-app>
</template>

<script>
import ProductManager from '@/components/productmanager.vue';

export default {
  name: 'App',
  components: {
    ProductManager,
  },
};
</script>
