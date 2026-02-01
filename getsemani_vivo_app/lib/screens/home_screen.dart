// lib/screens/home_screen.dart
// Pantalla principal con lista de negocios

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/auth_service.dart';
import '../services/business_service.dart';
import '../models/business.dart';
import '../utils/constants.dart';
import '../widgets/business_card.dart';
import 'business_detail_screen.dart';


class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  List<Business> _businesses = [];
  bool _isLoading = true;
  String? _selectedCategory;

  @override
  void initState() {
    super.initState();
    _loadBusinesses();
  }

  Future<void> _loadBusinesses() async {
    setState(() => _isLoading = true);
    
    final businesses = await BusinessService.getBusinesses(
      category: _selectedCategory,
    );
    
    if (mounted) {
      setState(() {
        _businesses = businesses;
        _isLoading = false;
      });
    }
  }

  void _selectCategory(String? category) {
    setState(() => _selectedCategory = category);
    _loadBusinesses();
  }


  @override
  Widget build(BuildContext context) {
    final authService = Provider.of<AuthService>(context);
    final user = authService.user;

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Getsemaní Vivo'),
        actions: const [],
      ),
      body: Column(
        children: [
          // Saludo al usuario
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(20),
            color: AppColors.primary,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '¡Hola, ${user?.fullName ?? 'Explorador'}! 👋',
                  style: const TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                    color: AppColors.white,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  'Descubre los mejores lugares de Getsemaní',
                  style: TextStyle(
                    fontSize: 14,
                    color: AppColors.white.withValues(alpha: 0.8),
                  ),
                ),
              ],
            ),
          ),

          // Filtro de categorías
          Container(
            height: 56,
            color: AppColors.white,
            child: ListView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              children: [
                _buildCategoryChip(null, 'Todos', Icons.apps),
                ...BusinessCategories.names.entries.map((entry) => 
                  _buildCategoryChip(
                    entry.key,
                    entry.value,
                    BusinessCategories.icons[entry.key] ?? Icons.place,
                  ),
                ),
              ],
            ),
          ),

          // Lista de negocios
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : _businesses.isEmpty
                    ? Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.store_outlined, size: 64, color: AppColors.textLight),
                            const SizedBox(height: 16),
                            const Text(
                              'No hay negocios disponibles',
                              style: AppTextStyles.bodySmall,
                            ),
                            const SizedBox(height: 8),
                            TextButton(
                              onPressed: _loadBusinesses,
                              child: const Text('Reintentar'),
                            ),
                          ],
                        ),
                      )
                    : RefreshIndicator(
                        onRefresh: _loadBusinesses,
                        child: ListView.builder(
                          padding: const EdgeInsets.all(16),
                          itemCount: _businesses.length,
                          itemBuilder: (context, index) {
                            return BusinessCard(
                              business: _businesses[index],
                              onTap: () {
                                Navigator.of(context).push(
                                  MaterialPageRoute(
                                    builder: (context) => BusinessDetailScreen(
                                      businessId: _businesses[index].id,
                                    ),
                                  ),
                                );
                              },
                            );
                          },
                        ),
                      ),
          ),
        ],
      ),
    );
  }

  Widget _buildCategoryChip(String? category, String label, IconData icon) {
    final isSelected = _selectedCategory == category;
    
    return Padding(
      padding: const EdgeInsets.only(right: 8),
      child: FilterChip(
        selected: isSelected,
        label: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 16, color: isSelected ? AppColors.white : AppColors.primary),
            const SizedBox(width: 4),
            Text(label),
          ],
        ),
        onSelected: (_) => _selectCategory(category),
        selectedColor: AppColors.primary,
        backgroundColor: AppColors.white,
        labelStyle: TextStyle(
          color: isSelected ? AppColors.white : AppColors.textPrimary,
          fontSize: 13,
        ),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
          side: BorderSide(
            color: isSelected ? AppColors.primary : Colors.grey.shade300,
          ),
        ),
      ),
    );
  }
}