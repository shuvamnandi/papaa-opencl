import numpy as np
import os, sys

def dump_conv_weights(net, layer_name, c_file_name, h_file_name):

    conv_weights = net.params[layer_name][0].data
    conv_bias = net.params[layer_name][1].data

    h_file = open(h_file_name, 'a')
    c_file = open(c_file_name, 'a')

    # write # defines related to conv layer params
    def_no_inputs = layer_name.upper() + '_NO_INPUTS'
    def_no_outputs = layer_name.upper() + '_NO_OUTPUTS'
    def_filter_h = layer_name.upper() + '_FILTER_HEIGHT'
    def_filter_w = layer_name.upper() + '_FILTER_WIDTH'

    h_file.write('#define '+ def_no_inputs+'  '+str(conv_weights.shape[1])+'\n\n')
    h_file.write('#define '+ def_no_outputs+'  '+str(conv_weights.shape[0])+'\n\n')
    h_file.write('#define ' + def_filter_h+ '  '+str(conv_weights.shape[2])+'\n\n')
    h_file.write('#define ' + def_filter_w+ '  '+str(conv_weights.shape[3])+'\n\n')

    # extern variable weight and bias array names
    h_file.write('extern const float ' + layer_name +'_weights' + 
        '[{:s}][{:s}*{:s}*{:s}];\n\n'.format(def_no_outputs, def_no_inputs, def_filter_h, def_filter_w))
    h_file.write('extern const float ' + layer_name + '_bias' + '[{:s}];\n\n'.format(def_no_outputs))

    # write weights to the C source file
    c_file.write('const float {:s}_weights[{:s}][{:s}*{:s}*{:s}] = '.format(layer_name, def_no_outputs, def_no_inputs, def_filter_h, def_filter_w) + '{\n')
    for f in range(conv_weights.shape[0]):
        c_file.write('{')
        filt = conv_weights[f].reshape(-1).tolist()
        for i, e in enumerate(filt):
            if(i == len(filt)-1):
                c_file.write('{:f}'.format(e))
            else:
                c_file.write('{:f}, '.format(e))
        if(f == conv_weights.shape[0]-1):
            c_file.write('}\n')
        else:
            c_file.write('},\n')
    c_file.write('};\n\n')

    # write bias to same file
    c_file.write('const float {:s}_bias [{:s}] = '.format(layer_name, def_no_outputs)+'{\n')
    bias = conv_bias.tolist()
    for i, b in enumerate(bias):
        if(i == len(bias)-1):
            c_file.write('{:f}'.format(b))
        else:
            c_file.write('{:f}, '.format(b))
    c_file.write('};\n\n')
    

    h_file.close()
    c_file.close()


def dump_ip_weights(net, layer_name, c_file_name, h_file_name):

    ip_weights = net.params[layer_name][0].data
    ip_bias = net.params[layer_name][1].data

    h_file = open(h_file_name, 'a')
    c_file = open(c_file_name, 'a')

    def_no_inputs = layer_name.upper() + '_NO_INPUTS'
    def_no_outputs = layer_name.upper() + '_NO_OUTPUTS'

    # write # defines related to conv layer params
    h_file.write('#define ' + def_no_inputs + '  '+str(ip_weights.shape[1])+'\n\n')
    h_file.write('#define ' + def_no_outputs +'  '+str(ip_weights.shape[0])+'\n\n')

    # extern variable weight and bias array names
    h_file.write('extern const float {:s}_weights[{:s}][{:s}];\n\n'.format(layer_name, def_no_outputs, def_no_inputs))
    h_file.write('extern const float {:s}_bias[{:s}];\n\n'.format(layer_name, def_no_outputs))

    # write weights to the C source file
    c_file.write('const float {:s}_weights[{:s}][{:s}] = '.format(layer_name, def_no_outputs, def_no_inputs)+'{\n')
    for f in range(ip_weights.shape[0]):
        c_file.write('{')
        filt = ip_weights[f].tolist()
        for i, e in enumerate(filt):
            if(i == len(filt)-1):
                c_file.write('{:f}'.format(e))
            else:
                c_file.write('{:f}, '.format(e))
        if(f == ip_weights.shape[0]-1):
            c_file.write('}\n')
        else:
            c_file.write('},\n')
    c_file.write('};\n\n')

    # write bias to same file
    c_file.write('const float {:s}_bias[{:s}] = '.format(layer_name, def_no_outputs)+'{\n')
    bias = ip_bias.tolist()
    for i, b in enumerate(bias):
        if(i == len(bias)-1):
            c_file.write('{:f}'.format(b))
        else:
            c_file.write('{:f}, '.format(b))
    c_file.write('};\n\n')
    

    h_file.close()
    c_file.close()
