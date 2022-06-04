from MapLegacy import MapLegacy


def main():
    converter = MapLegacy("Maps/radar_final.map")
    converter.build("radar_noterrain")


if __name__ == '__main__':
    main()
