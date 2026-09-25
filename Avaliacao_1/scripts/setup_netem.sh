#!/bin/bash
# ==============================================================================
# setup_netem.sh - Configuracao de Emulacao de Canal (Traffic Control / Netem)
# ==============================================================================
# Uso:
#   ./setup_netem.sh clear              -> Remove todas as regras na eth0
#   ./setup_netem.sh scenario_a         -> Cenário A: Latencia < 5ms, 0% perda
#   ./setup_netem.sh scenario_b         -> Cenário B: RTT 20ms, 0% perda
#   ./setup_netem.sh scenario_c_loss0   -> Cenário C: RTT 100ms, 0% perda
#   ./setup_netem.sh scenario_c_loss2   -> Cenário C: RTT 100ms, 2% perda
#   ./setup_netem.sh scenario_c_loss5   -> Cenário C: RTT 100ms, 5% perda
#   ./setup_netem.sh show               -> Exibe qdisc atual
# ==============================================================================

IFACE="${NETEM_IFACE:-eth0}"
CMD="$1"

clear_rules() {
    # Evita silenciamento cego com || true; verifica se há qdisc raiz customizada instalada
    if tc qdisc show dev "${IFACE}" 2>/dev/null | grep -q "netem"; then
        echo "[NETEM] Removendo regra netem em ${IFACE}..."
        tc qdisc del dev "${IFACE}" root
    fi
}

case "$CMD" in
    clear)
        clear_rules
        echo "[NETEM] Interface ${IFACE} em estado limpo (sem emulacao)."
        ;;
    scenario_a)
        clear_rules
        echo "[NETEM] Aplicando Cenario A: Atraso 2ms (RTT ~4ms), 0% perda..."
        tc qdisc add dev ${IFACE} root netem delay 2ms
        ;;
    scenario_b)
        clear_rules
        echo "[NETEM] Aplicando Cenario B: Atraso 10ms (RTT ~20ms), 0% perda..."
        tc qdisc add dev ${IFACE} root netem delay 10ms
        ;;
    scenario_c_loss0)
        clear_rules
        echo "[NETEM] Aplicando Cenario C (Loss 0%): Atraso 50ms (RTT ~100ms), 0% perda..."
        tc qdisc add dev ${IFACE} root netem delay 50ms
        ;;
    scenario_c_loss2)
        clear_rules
        echo "[NETEM] Aplicando Cenario C (Loss 2%): Atraso 50ms (RTT ~100ms), 2% perda aleatoria..."
        tc qdisc add dev ${IFACE} root netem delay 50ms loss 2%
        ;;
    scenario_c_loss5)
        clear_rules
        echo "[NETEM] Aplicando Cenario C (Loss 5%): Atraso 50ms (RTT ~100ms), 5% perda aleatoria..."
        tc qdisc add dev ${IFACE} root netem delay 50ms loss 5%
        ;;
    show)
        echo "[NETEM] Regras ativas em ${IFACE}:"
        tc -s qdisc show dev ${IFACE}
        ;;
    *)
        echo "Uso: $0 {clear|scenario_a|scenario_b|scenario_c_loss0|scenario_c_loss2|scenario_c_loss5|show}"
        exit 1
        ;;
esac
