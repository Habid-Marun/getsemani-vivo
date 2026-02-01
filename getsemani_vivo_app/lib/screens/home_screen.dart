// lib/screens/home_screen.dart
// Pantalla principal (temporal)

import 'package:flutter/material.dart';
import '../utils/constants.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Getsemaní Vivo'),
      ),
      body: Center(
        child: Text(
          'Pantalla Principal\n(Próximo paso)',
          textAlign: TextAlign.center,
          style: AppTextStyles.heading2,
        ),
      ),
    );
  }
}