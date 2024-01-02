class Utils:

    def verify_search_results(self, all_stops1):
        for stops in all_stops1:
            if(stops.text!='1 Stop'):
                assert False
