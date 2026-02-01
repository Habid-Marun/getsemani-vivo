// lib/screens/points_screen.dart
// Pantalla de mis puntos

import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:http/http.dart' as http;
import '../services/auth_service.dart';
import '../utils/constants.dart';

class PointsScreen extends StatefulWidget {
  const PointsScreen({super.key});

  @override
  State<PointsScreen> createState() => _PointsScreenState();
}

class _PointsScreenState extends State<PointsScreen> {
  Map<String, dynamic>? _pointsSummary;
  List<dynamic> _history = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadPoints();
  }

  Future<void> _loadPoints() async {
    setState(() => _isLoading = true);

    final authService = Provider.of<AuthService>(context, listen: false);
    final token = authService.token;

    try {
      // Obtener resumen de puntos
      final summaryResponse = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.myPoints}'),
        headers: {'Authorization': 'Bearer $token'},
      );

      // Obtener historial
      final historyResponse = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.myPoints}/history'),
        headers: {'Authorization': 'Bearer $token'},
      );

      if (mounted) {
        setState(() {
          if (summaryResponse.statusCode == 200) {
            _pointsSummary = json.decode(summaryResponse.body);
          }
          if (historyResponse.statusCode == 200) {
            _history = json.decode(historyResponse.body);
          }
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Mis Puntos'),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _loadPoints,
              child: SingleChildScrollView(
                physics: const AlwaysScrollableScrollPhysics(),
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Tarjeta de puntos totales
                    _buildTotalPointsCard(),
                    const SizedBox(height: 24),

                    // Puntos por negocio
                    if (_pointsSummary != null &&
                        _pointsSummary!['points_by_business'] != null &&
                        (_pointsSummary!['points_by_business'] as List).isNotEmpty)
                      _buildPointsByBusiness(),

                    // Historial
                    const Text('Historial de Consumos', style: AppTextStyles.heading3),
                    const SizedBox(height: 12),

                    if (_history.isEmpty)
                      Center(
                        child: Padding(
                          padding: const EdgeInsets.all(40),
                          child: Column(
                            children: [
                              Icon(Icons.receipt_long, size: 64, color: AppColors.textLight),
                              const SizedBox(height: 16),
                              const Text(
                                'Aún no tienes consumos',
                                style: AppTextStyles.bodySmall,
                              ),
                              const SizedBox(height: 8),
                              const Text(
                                'Visita negocios de Getsemaní y acumula puntos',
                                style: AppTextStyles.bodySmall,
                                textAlign: TextAlign.center,
                              ),
                            ],
                          ),
                        ),
                      )
                    else
                      ..._history.map((item) => _buildHistoryItem(item)),
                  ],
                ),
              ),
            ),
    );
  }

  Widget _buildTotalPointsCard() {
    final totalPoints = _pointsSummary?['total_points'] ?? 0;
    final totalSpent = _pointsSummary?['total_spent'] ?? 0.0;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [AppColors.primary, Color(0xFF2874A6)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: AppColors.primary.withValues(alpha: 0.3),
            blurRadius: 15,
            offset: const Offset(0, 8),
          ),
        ],
      ),
      child: Column(
        children: [
          const Text(
            'Puntos Acumulados',
            style: TextStyle(color: Colors.white70, fontSize: 16),
          ),
          const SizedBox(height: 8),
          Text(
            '$totalPoints',
            style: const TextStyle(
              color: AppColors.white,
              fontSize: 56,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 4),
          const Text(
            'puntos',
            style: TextStyle(color: Colors.white70, fontSize: 16),
          ),
          const SizedBox(height: 16),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            decoration: BoxDecoration(
              color: AppColors.white.withValues(alpha: 0.2),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Text(
              'Total gastado: \$${totalSpent.toStringAsFixed(0)} COP',
              style: const TextStyle(color: AppColors.white, fontSize: 14),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPointsByBusiness() {
    final businesses = _pointsSummary!['points_by_business'] as List;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Puntos por Negocio', style: AppTextStyles.heading3),
        const SizedBox(height: 12),
        ...businesses.map((b) => Container(
              margin: const EdgeInsets.only(bottom: 8),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: AppColors.white,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                children: [
                  Container(
                    width: 44,
                    height: 44,
                    decoration: BoxDecoration(
                      color: AppColors.primary.withValues(alpha: 0.1),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Icon(Icons.store, color: AppColors.primary),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          b['business_name'] ?? 'Negocio',
                          style: const TextStyle(fontWeight: FontWeight.w600),
                        ),
                        Text(
                          '${b['visits'] ?? 0} visitas',
                          style: AppTextStyles.bodySmall,
                        ),
                      ],
                    ),
                  ),
                  Text(
                    '${b['points'] ?? 0} pts',
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: AppColors.primary,
                    ),
                  ),
                ],
              ),
            )),
        const SizedBox(height: 24),
      ],
    );
  }

  Widget _buildHistoryItem(dynamic item) {
    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.white,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        children: [
          Container(
            width: 44,
            height: 44,
            decoration: BoxDecoration(
              color: AppColors.success.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Icon(Icons.add_circle, color: AppColors.success),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  item['business_name'] ?? 'Negocio',
                  style: const TextStyle(fontWeight: FontWeight.w600),
                ),
                Text(
                  '\$${(item['amount'] ?? 0).toStringAsFixed(0)} COP',
                  style: AppTextStyles.bodySmall,
                ),
              ],
            ),
          ),
          Text(
            '+${item['points_earned'] ?? 0}',
            style: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: AppColors.success,
            ),
          ),
        ],
      ),
    );
  }
}