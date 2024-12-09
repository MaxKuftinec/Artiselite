<template>
  <v-layout>
    <v-navigation-drawer v-model="drawer">
      <v-list density="compact" item-props :items="items" nav />

      <template #append>
        <v-list-item
          class="ma-2"
          link
          nav
          prepend-icon="mdi-cog-outline"
          title="Settings"
        />
      </template>
    </v-navigation-drawer>

    <v-app-bar border="b" class="ps-4" flat>
      <v-app-bar-nav-icon v-if="$vuetify.display.smAndDown" @click="drawer = !drawer" />

      <v-app-bar-title>Warehouse Inventory</v-app-bar-title>

      <template #append>
        <v-btn class="text-none me-2" height="48" icon slim>
          <v-avatar color="surface-light" size="32">
						<v-icon>mdi-account-tie</v-icon>
					</v-avatar>

          <v-menu activator="parent">
            <v-list density="compact" nav>
              <v-list-item append-icon="mdi-cog-outline" link title="Settings" />

              <v-list-item append-icon="mdi-logout" link title="Logout" @click="logout"/>
            </v-list>
          </v-menu>
        </v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <div class="pa-4">
        <v-sheet
          border="dashed md"
          color="surface-light"
          rounded="lg"
          width="100%"
        >
					<v-form v-model="valid" @keyup.enter="addProduct">
						<v-text-field
							v-model="newProduct.name"
							label="Product Name"
							required
						></v-text-field>

						<v-text-field
							v-model="newProduct.quantity"
							label="Quantity"
							type="number"
							:rules="[value => value >= 0 || 'Must be a positive number']"
							min="0"
							required
						></v-text-field>

						<v-btn @click="addProduct" :disabled="!valid">Add Product</v-btn>
					</v-form>

					<v-text-field v-slot:text
						v-model="search"
						label="Search"
						prepend-inner-icon="mdi-magnify"
						single-line
						clearable
					></v-text-field>

					<v-data-table
            :headers="headers"
            :items="products"
						:search="search"
					>
						<template v-slot:top>
							<v-toolbar flat style="border: 1px solid black;">
								<v-toolbar-title>Products</v-toolbar-title>
							</v-toolbar>
						</template>

						<template v-slot:item.actions="{ item }">
							<v-icon @click="editProduct(item)">mdi-pencil</v-icon>
							<v-icon @click="deleteProduct(item)">mdi-delete</v-icon>
						</template>

						<template v-slot:item.name="{ item }">
							<template v-if="item.isEditing">
								<v-text-field v-model="item.name" density="compact" @keyup.enter="editProduct(item)"></v-text-field>
							</template>
							<template v-else>
								{{ item.name }}
							</template>
						</template>

						<template v-slot:item.quantity="{ item }">
							<template v-if="item.isEditing">
								<v-text-field v-model="item.quantity" type="number" density="compact" :rules="[value => value >= 0 || 'Must be a positive number']" min="0" @keyup.enter="editProduct(item)"></v-text-field>
							</template>
							<template v-else>
								{{ item.quantity }}
							</template>
						</template>


					</v-data-table>
				</v-sheet>
      </div>
    </v-main>
  </v-layout>
</template>

<script>
	import{ useConfirm } from '@/../node_modules/vuetify-use-dialog/dist/vuetify-use-dialog.js';
	import { useUserStore } from '@/stores/users';
	import axios from "axios";

	const API_BASE_URL = import.meta.env.VITE_API_URL;

	export default {
		setup() {
			const confirm = useConfirm();
			return { confirm };
		},

		data() {
			return {
				valid: false,
				newProduct: {
					name: '',
					quantity: 0
				},
				products: [],
				headers: [
					{ title: 'Name', key: 'name'},
					{ title: 'Quantity', key: 'quantity'},
					{ title: 'Edit', key: 'actions', sortable: false}
				],
				items: [
					{
						title: 'Inventory',
						prependIcon: 'mdi-view-dashboard-outline',
						to: '/'
					},
					{
						title: 'Team',
						prependIcon: 'mdi-account-group',
						to: '/team'
					},
					{
						title: 'Inbound',
						prependIcon: 'mdi-bank-transfer-in',
						to: '/inbound'
					},
					{
						title: 'Outbound',
						prependIcon: 'mdi-bank-transfer-out',
						to: '/outbound'
					}
				],
				drawer: true,
				search: '',
			}
		},

		methods: {
			addProduct() {
				if (this.newProduct.name && this.newProduct.quantity >= 0) {
					this.newProduct.quantity = parseInt(this.newProduct.quantity);
					this.postProducts(this.newProduct);
					this.fetchProducts(); // It could be done this way, but I think it's better to add it immedeately to the product object
					this.newProduct.name = '';
					this.newProduct.quantity = 0;
				}
			},
			
      editProduct(item) {
				// This if block is where we want to call the put api method
				if (item.isEditing) {
					// console.log(item);
					delete item.isEditing;
					this.putProduct(item);
					return ;
				}
				item.quantity = parseInt(item.quantity);
				if (item.quantity >= 0 && item.quantity != NaN) {
					item.isEditing = !item.isEditing;
				}
      },

			async deleteProduct(item) {
				const res = await this.confirm({ content: `Delete product: ${item.name}?`, title: 'Delete Confirmation' });
				if (res) {
					// const index = this.products.indexOf(item); // Why need this?
					// if (index > -1) { // Activate this if above line is activated
					try {
						const	response = await axios.delete(`${API_BASE_URL}/products/${item.id}`);
						if (response.status === 200)
							// this.products.splice(index, 1); // What's emit? this.@emit('updated-product', this.products)
							this.fetchProducts();
						else
							console.error("Failed to remove item:", respnse.data);
					}
					catch (error) {
						console.error("Error removing item from product:", error.response ? error.response.data : error.message);
					}
					// } Activate this if the if block is activated
				}
			},

			async putProduct(item) {
				try {
					const response = await axios.put(`${API_BASE_URL}/products/${item.id}`, item);
					if (response.status !== 200)
						console.error("Failed to update product", response.data);
				}
				catch (error) {
          console.error("Error updating product:", error.response? error.response.data : error.message);
        }
			},

			// For some reason, every character that is written in the text field will trigger this function 3 times where products is iterated by all products key
			// Apparently, this is not needed
			customFilter(products, search, key) {
				if (key.columns.name == products){
					console.log("Are you serious?");
					console.log(`search: ${search}`);
					console.log(`products: ${products}`);
					console.log(`key: ${JSON.stringify(key)}`);
					console.log(key.columns);
					console.log(key.columns.name);

					return (key.columns);

					const searchLower = search.toLowerCase();
					// return products.filter(item => item[key].toLowerCase().includes(searchLower));
				}
			},

			async fetchProducts() {
				try {
					const response = await axios.get(`${API_BASE_URL}/products`);
					this.products = response.data;
					// console.log(this.products);
				}
				catch (error) {
          console.error("Error fetching products ley:", error);
        }
			},

			async postProducts(newProduct) {
				try {
					const response = await axios.post(`${API_BASE_URL}/products`, newProduct);
				}
				catch (error) {
          console.error("Error posting product ley:", error);
					if (error.response) {
						const statusCode = error.response.status;
						if (statusCode === 400) {
							this.$toast.error("Invalid data. Please check your input");
						}
					else
						this.$toast.error("Failed to add item");
					}
        }
			},

			logout() {
				const userStore = useUserStore();
				userStore.logout();
				this.$router.push('/login');
			}
		},

		mounted() {
			this.fetchProducts();
		}
	};
</script>
