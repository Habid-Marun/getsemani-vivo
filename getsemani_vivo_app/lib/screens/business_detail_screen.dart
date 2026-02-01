// lib/screens/business_detail_screen.dart
// Pantalla de detalle de negocio

import 'package:flutter/material.dart';
import '../services/business_service.dart';
import '../models/business.dart';
import '../utils/constants.dart';

class BusinessDetailScreen extends StatefulWidget {
  final int businessId;

  const BusinessDetailScreen({
    super.key,
    required this.businessId,
  });

  @override
  State<BusinessDetailScreen> createState() => _BusinessDetailScreenState();
}

class _BusinessDetailScreenState extends State<BusinessDetailScreen> {
  Business? _business;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadBusiness();
  }

  Future<void> _loadBusiness() async {
    final business = await BusinessService.getBusiness(widget.businessId);
    if (mounted) {
      setState(() {
        _business = business;
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        appBar: AppBar(),
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    if (_business == null) {
      return Scaffold(
        appBar: AppBar(),
        body: const Center(child: Text('Negocio no encontrado')),
      );
    }

    final business = _business!;

    return Scaffold(
      backgroundColor: AppColors.background,
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 250,
            pinned: true,
            flexibleSpace: FlexibleSpaceBar(
              background: business.primaryImageUrl != null
                  ? Image.network(
                      '${ApiConfig.baseUrl}${business.primaryImageUrl}',
                      fit: BoxFit.cover,
                      errorBuilder: (context, error, stackTrace) =>
                          _buildImagePlaceholder(business),
                    )
                  : _buildImagePlaceholder(business),
            ),
          ),
          SliverToBoxAdapter(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(20),
                  color: AppColors.white,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Expanded(
                            child: Text(
                              business.name,
                              style: AppTextStyles.heading1,
                            ),
                          ),
                          if (business.isFeatured)
                            Container(
                              padding: const EdgeInsets.symmetric(
                                  horizontal: 10, vertical: 6),
                              decoration: BoxDecoration(
                                color: AppColors.accent,
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: const Text(
                                '⭐ Destacado',
                                style: TextStyle(
                                  color: AppColors.white,
                                  fontSize: 12,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      Row(
                        children: [
                          Icon(
                            BusinessCategories.icons[business.category] ??
                                Icons.place,
                            size: 20,
                            color: AppColors.primary,
                          ),
                          const SizedBox(width: 6),
                          Text(
                            BusinessCategories.names[business.category] ??
                                business.category,
                            style: const TextStyle(
                              fontSize: 16,
                              color: AppColors.primary,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 12),
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 12, vertical: 8),
                        decoration: BoxDecoration(
                          color: AppColors.success.withValues(alpha: 0.1),
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const Icon(Icons.stars,
                                color: AppColors.success, size: 20),
                            const SizedBox(width: 6),
                            Text(
                              '${business.pointsPer10000} punto(s) por cada \$10,000 COP',
                              style: const TextStyle(
                                color: AppColors.success,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 12),
                if (business.description != null &&
                    business.description!.isNotEmpty)
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(20),
                    color: AppColors.white,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('Descripción', style: AppTextStyles.heading3),
                        const SizedBox(height: 8),
                        Text(business.description!, style: AppTextStyles.body),
                      ],
                    ),
                  ),
                const SizedBox(height: 12),
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(20),
                  color: AppColors.white,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Información', style: AppTextStyles.heading3),
                      const SizedBox(height: 12),
                      _buildInfoRow(Icons.location_on, business.address),
                      if (business.phone != null)
                        _buildInfoRow(Icons.phone, business.phone!),
                      if (business.email != null)
                        _buildInfoRow(Icons.email, business.email!),
                      if (business.website != null)
                        _buildInfoRow(Icons.language, business.website!),
                      if (business.instagram != null)
                        _buildInfoRow(Icons.camera_alt, business.instagram!),
                    ],
                  ),
                ),
                const SizedBox(height: 40),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInfoRow(IconData icon, String text) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        children: [
          Icon(icon, size: 20, color: AppColors.primary),
          const SizedBox(width: 12),
          Expanded(
            child: Text(text, style: AppTextStyles.body),
          ),
        ],
      ),
    );
  }

  Widget _buildImagePlaceholder(Business business) {
    return Container(
      color: AppColors.primary.withValues(alpha: 0.1),
      child: Center(
        child: Icon(
          BusinessCategories.icons[business.category] ?? Icons.store,
          size: 64,
          color: AppColors.primary.withValues(alpha: 0.3),
        ),
      ),
    );
  }
}