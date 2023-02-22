from braket.aws import AwsDevice
from braket.ocean_plugin import BraketSampler, BraketDWaveSampler
from dwave.system.composites import EmbeddingComposite

NUM_READS = 100

def anneal(model):
    my_bucket = "amazon-braket-rmeadowc" 
    my_prefix = "/jobs" 
    s3_folder = (my_bucket, my_prefix)

    #DWave_device='DW_2000Q_6' #if using 2000Q
    DWave_device='Advantage_system6.1' #if using advantage 6.1
    #DWave_device='Advantage_system4.1' #if using advantage 4.1
    # Please run available_devices() to validate the latest QPU available and edit the above list
    device =AwsDevice.get_devices(names=DWave_device)[0]
    sampler = BraketDWaveSampler(s3_folder,device.arn)
    sampler = EmbeddingComposite(sampler)
    #max_shots=device.properties.service.shotsRange[1]
    #print('Number of qubits: ',device.properties.provider.qubitCount)
    #print('Number of couplers',len(device.properties.provider.couplers))
    #print('Shots max {:,}'.format(max_shots) )

    #chainstrength = 1
    response = sampler.sample(model, num_reads=NUM_READS)
    print(response)

    res = next(response.data())[0]

    selected_nodes = []
    for var in res:
        if var.isdigit() and res[var]==1:
            selected_nodes.append(int(var))

    return selected_nodes

