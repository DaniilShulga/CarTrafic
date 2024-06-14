import traci
import sumolib

# Путь к файлу конфигурации SUMO
sumo_config_file = 'C:\\Users\\dr_sh\\Sumo\\2024-06-14-16-09-15\\osm.sumocfg'

# Запуск SUMO в фоновом режиме
sumo_cmd = ['sumo-gui', '-c', sumo_config_file]
traci.start(sumo_cmd)

# Идентификаторы дорог, образующих перекресток
incoming_edges = ['-390311740#8', '390311740#3', '-35854637#3']
traffic_light_id = '419055954'  # Замените на ваш идентификатор светофора

# Пороговое значение для определения затора
congestion_threshold = 3  # Замените на ваше пороговое значение

# Длительности фаз светофора
default_green_duration = 30  # Длительность зеленого света по умолчанию
reduced_green_duration = 10  # Уменьшенная длительность зеленого света

# Счетчик автомобилей
traffic_count = {edge: 0 for edge in incoming_edges}

try:
    # Основной цикл симуляции
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()  # Шаг симуляции

        # Подсчет автомобилей на каждой дороге
        total_vehicles = 0
        for edge in incoming_edges:
            vehicles_on_edge = traci.edge.getLastStepVehicleIDs(edge)
            traffic_count[edge] += len(vehicles_on_edge)
            total_vehicles += len(vehicles_on_edge)

        # Проверка на затор
        if total_vehicles > congestion_threshold:
            print(f"Step {step}: Congestion detected, setting reduced green duration")
            traci.trafficlight.setPhaseDuration(traffic_light_id, reduced_green_duration)
        else:
            print(f"Step {step}: No congestion, setting default green duration")
            traci.trafficlight.setPhaseDuration(traffic_light_id, default_green_duration)

        # Проверка текущей фазы светофора
        current_phase = traci.trafficlight.getPhase(traffic_light_id)
        print(f"Step {step}: Current phase for {traffic_light_id}: {current_phase}")

        # Вывод результатов на каждом шаге
        print(f"Step {step}:")
        for edge, count in traffic_count.items():
            print(f"  Total vehicles passed through {edge}: {count}")
        print("\n")
        step += 1

finally:
    traci.close()  # Закрытие соединения с SUMO

    # Итоговый вывод результатов
    print("Final results:")
    for edge, count in traffic_count.items():
        print(f"Total vehicles passed through {edge}: {count}")
