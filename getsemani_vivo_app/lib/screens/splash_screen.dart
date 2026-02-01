// lib/screens/splash_screen.dart
// Pantalla de carga inicial

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/auth_service.dart';
import '../utils/constants.dart';
import 'login_screen.dart';
import 'home_screen.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    _checkAuth();
  }

  Future<void> _checkAuth() async {
    // Esperar un momento para mostrar el logo
    await Future.delayed(const Duration(seconds: 2));
    
    if (!mounted) return;
    
    // Verificar si hay sesión guardada
    final authService = Provider.of<AuthService>(context, listen: false);
    final isAuthenticated = await authService.initialize();
    
    if (!mounted) return;
    
    // Navegar a la pantalla correspondiente
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(
        builder: (context) => isAuthenticated ? const HomeScreen() : const LoginScreen(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.primary,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Logo o ícono
            Container(
              width: 120,
              height: 120,
              decoration: BoxDecoration(
                color: AppColors.white,
                borderRadius: BorderRadius.circular(30),
              ),
              child: const Icon(
                Icons.location_city,
                size: 60,
                color: AppColors.primary,
              ),
            ),
            const SizedBox(height: 24),
            
            // Nombre de la app
            const Text(
              'Getsemaní',
              style: TextStyle(
                fontSize: 36,
                fontWeight: FontWeight.bold,
                color: AppColors.white,
              ),
            ),
            const Text(
              'Vivo',
              style: TextStyle(
                fontSize: 36,
                fontWeight: FontWeight.w300,
                color: AppColors.accent,
              ),
            ),
            const SizedBox(height: 8),
            
            // Subtítulo
            Text(
              'Descubre el corazón de Cartagena',
              style: TextStyle(
                fontSize: 16,
                color: AppColors.white.withValues(alpha: 0.8),
              ),
            ),
            const SizedBox(height: 48),
            
            // Indicador de carga
            const CircularProgressIndicator(
              valueColor: AlwaysStoppedAnimation<Color>(AppColors.white),
            ),
          ],
        ),
      ),
    );
  }
}