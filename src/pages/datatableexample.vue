<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="items"
      :items-per-page="5"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Data Table Example</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            label="Search"
            single-line
            clearable
          ></v-text-field>
        </v-toolbar>
      </template>

      <template v-slot:item.actions="{ item }">
        <v-icon small @click="editItem(item)">mdi-pencil</v-icon>
        <v-icon small @click="deleteItem(item)">mdi-delete</v-icon>
      </template>

      <template v-slot:no-data>
        <v-btn color="primary" @click="initialize">Reset Data</v-btn>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      search: "",
      headers: [
        { title: "Name", key: "name" },
        { title: "Age", key: "age" },
        { title: "Email", key: "email" },
        { title: "Actions", key: "actions", sortable: false },
      ],
      items: [
        { name: "Alice", age: 25, email: "alice@example.com" },
        { name: "Bob", age: 30, email: "bob@example.com" },
        { name: "Charlie", age: 35, email: "charlie@example.com" },
        { name: "Diana", age: 28, email: "diana@example.com" },
      ],
    };
  },
  methods: {
    editItem(item) {
      console.log("Editing item:", item);
    },
    deleteItem(item) {
      const index = this.items.indexOf(item);
      if (index > -1) {
        this.items.splice(index, 1);
      }
    },
    initialize() {
      this.items = [
        { name: "Alice", age: 25, email: "alice@example.com" },
        { name: "Bob", age: 30, email: "bob@example.com" },
        { name: "Charlie", age: 35, email: "charlie@example.com" },
        { name: "Diana", age: 28, email: "diana@example.com" },
      ];
    },
  },
};
</script>

<style>
/* Add any custom styling if needed */
</style>
