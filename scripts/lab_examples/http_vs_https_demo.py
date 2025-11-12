#!/usr/bin/env python3
"""
HTTP vs HTTPS Demo - Demonstração Educacional

Demonstra visualmente a diferença entre tráfego HTTP e HTTPS.
Perfeito para ensinar crianças sobre criptografia.

Usage:
    sudo python3 http_vs_https_demo.py

Author: Professor JuanCS-Dev ✝️
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.education import WiFiLabInterceptor


def print_banner():
    """Banner educacional"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║              🔒 HTTP vs HTTPS - Demonstração Visual 🔒               ║
║                                                                      ║
║  Veja a diferença entre conexões seguras e inseguras                ║
╚══════════════════════════════════════════════════════════════════════╝
    """)


def explain_http():
    """Explica HTTP"""
    print("\n" + "="*70)
    print("📖 PARTE 1: O que é HTTP?")
    print("="*70)
    print("""
HTTP = HyperText Transfer Protocol

🔓 É como enviar uma CARTA SEM ENVELOPE:
   ├─ Qualquer pessoa pode ler
   ├─ Não há proteção
   ├─ Dados em texto claro
   └─ PERIGOSO! ⚠️

Exemplo de dados HTTP (TODOS podem ver):
┌──────────────────────────────────────────────────┐
│ GET /login HTTP/1.1                              │
│ Host: exemplo.com                                │
│ username=joao&password=senha123                  │
└──────────────────────────────────────────────────┘
    """)
    input("\n📚 Pressione ENTER para continuar...")


def explain_https():
    """Explica HTTPS"""
    print("\n" + "="*70)
    print("📖 PARTE 2: O que é HTTPS?")
    print("="*70)
    print("""
HTTPS = HTTP + SSL/TLS (Criptografia)

🔒 É como enviar uma CARTA LACRADA:
   ├─ Apenas destinatário pode ler
   ├─ Dados criptografados
   ├─ Certificado de segurança
   └─ SEGURO! ✅

Exemplo de dados HTTPS (NINGUÉM pode ler):
┌──────────────────────────────────────────────────┐
│ ���x&7#�2K�@���%$#*&���)(�7�&��*��%#            │
│ ��*#&#(�*%$)#*@)%)#�*3$)#*                       │
└──────────────────────────────────────────────────┘

Parece código maluco? É porque está CRIPTOGRAFADO! 🔒
    """)
    input("\n📚 Pressione ENTER para continuar...")


def live_demo():
    """Demonstração ao vivo"""
    print("\n" + "="*70)
    print("🔬 PARTE 3: Demonstração ao Vivo")
    print("="*70)
    print("""
Agora vamos CAPTURAR TRÁFEGO REAL!

📱 INSTRUÇÕES:
   1. Pegue seu celular/tablet
   2. Quando eu disser, acesse: http://neverssl.com
   3. Observe o que consigo ver!
   4. Depois acesse: https://google.com
   5. Veja a diferença!
    """)
    
    input("\n🚀 Pressione ENTER para INICIAR a captura...")
    
    # Cria interceptador
    lab = WiFiLabInterceptor(interface="wlan0", lab_mode=True)
    
    print("\n🎯 CAPTURA INICIADA!")
    print("   Agora acesse os sites nos dispositivos...\n")
    
    # Captura por 45 segundos
    lab.start_capture(duration=45, packet_count=500)
    
    return lab


def show_results(lab):
    """Mostra resultados da demonstração"""
    print("\n" + "="*70)
    print("📊 RESULTADOS DA DEMONSTRAÇÃO")
    print("="*70)
    
    http_count = lab.stats['http_packets']
    https_count = lab.stats['https_packets']
    
    print(f"\n⚠️  HTTP (INSEGURO): {http_count} pacotes")
    print(f"✅ HTTPS (SEGURO): {https_count} pacotes")
    
    if http_count > 0:
        print("\n🚨 ATENÇÃO! Detectamos tráfego HTTP!")
        print("   Em WiFi público, EU VERIA:")
        print("   - Sites exatos acessados")
        print("   - Dados enviados (senhas, mensagens)")
        print("   - Cookies de sessão")
        print("   - TUDO em texto claro!")
    
    if https_count > 0:
        print("\n✅ Parabéns! Tráfego HTTPS detectado!")
        print("   Com HTTPS, eu SÓ vejo:")
        print("   - IP do servidor")
        print("   - Quantidade de dados")
        print("   - Horário da conexão")
        print("   ❌ NÃO vejo conteúdo, senhas, mensagens!")
    
    print("\n" + "="*70)


def quiz():
    """Quiz educacional"""
    print("\n" + "="*70)
    print("🎓 QUIZ EDUCACIONAL")
    print("="*70)
    
    questions = [
        {
            'q': 'Qual é mais seguro: HTTP ou HTTPS?',
            'a': 'HTTPS',
            'explanation': 'HTTPS usa criptografia para proteger seus dados!'
        },
        {
            'q': 'Como saber se um site é HTTPS? (dica: olhe no navegador)',
            'a': 'cadeado',
            'explanation': 'O cadeado 🔒 ao lado da URL indica HTTPS!'
        },
        {
            'q': 'É seguro usar WiFi público aberto?',
            'a': 'não',
            'explanation': 'NUNCA! Qualquer pessoa pode interceptar seus dados!'
        }
    ]
    
    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\n❓ Pergunta {i}: {q['q']}")
        answer = input("   Sua resposta: ").strip().lower()
        
        if q['a'].lower() in answer:
            score += 1
            print("   ✅ CORRETO!")
        else:
            print(f"   ❌ Resposta: {q['a']}")
        
        print(f"   💡 {q['explanation']}")
    
    print("\n" + "="*70)
    print(f"🏆 Pontuação: {score}/{len(questions)}")
    
    if score == len(questions):
        print("🎉 PERFEITO! Você é um expert em segurança!")
    elif score >= len(questions) // 2:
        print("👍 Muito bem! Continue aprendendo!")
    else:
        print("📚 Continue estudando! Segurança é importante!")
    
    print("="*70)


def main():
    """Executa demonstração completa"""
    
    # Verifica root
    if os.geteuid() != 0:
        print("❌ Este script precisa ser executado com sudo")
        print("💡 Comando: sudo python3 http_vs_https_demo.py")
        sys.exit(1)
    
    print_banner()
    
    print("\n🎓 Bem-vindos ao Laboratório de Segurança WiFi!")
    print("   Hoje vamos aprender sobre HTTP vs HTTPS\n")
    
    input("📚 Pressione ENTER para começar a aula...")
    
    # Parte teórica
    explain_http()
    explain_https()
    
    # Demonstração prática
    lab = live_demo()
    
    # Resultados
    show_results(lab)
    
    # Quiz
    quiz()
    
    # Mensagem final
    print("\n" + "="*70)
    print("🎓 LIÇÃO APRENDIDA:")
    print("="*70)
    print("""
1. ✅ SEMPRE use HTTPS (procure o cadeado 🔒)
2. ❌ NUNCA confie em HTTP
3. 🚫 NUNCA use WiFi público sem proteção
4. 🔐 Use VPN quando necessário
5. 💡 Ensine seus amigos sobre segurança!
    """)
    print("="*70)
    
    print("\n🎉 Aula concluída! Parabéns!")
    print("📧 Dúvidas? Pergunte aos pais!\n")


if __name__ == "__main__":
    main()
